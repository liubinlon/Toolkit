//
// Copyright 2018 Pixar
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
#include "diagnosticDelegate.h"

#include <mayaUsd/base/debugCodes.h>

#include <pxr/base/arch/threads.h>
#include <pxr/base/tf/envSetting.h>
#include <pxr/base/tf/stackTrace.h>

#include <maya/MGlobal.h>

#include <ghc/filesystem.hpp>

PXR_NAMESPACE_OPEN_SCOPE

TF_DEFINE_ENV_SETTING(
    PIXMAYA_DIAGNOSTICS_BATCH,
    true,
    "Whether to batch diagnostics coming from the same call site. "
    "If batching is off, all secondary threads' diagnostics will be "
    "printed to stderr.");

TF_DEFINE_ENV_SETTING(
    MAYAUSD_SHOW_FULL_DIAGNOSTICS,
    false,
    "This env flag controls the granularity of TF error/warning/status messages "
    "being displayed in Maya.");

// Globally-shared delegate. Uses shared_ptr so we can have weak ptrs.
static std::shared_ptr<UsdMayaDiagnosticDelegate> _sharedDelegate;

// The delegate can be installed by multiple plugins (e.g. pxrUsd and
// mayaUsdPlugin), so keep track of installations to ensure that we only add
// the delegate for the first installation call, and that we only remove it for
// the last removal call.
static int _installationCount = 0;

namespace {

class _StatusOnlyDelegate : public UsdUtilsCoalescingDiagnosticDelegate
{
    void IssueWarning(const TfWarning&) override { }
    void IssueFatalError(const TfCallContext&, const std::string&) override { }
};

class _WarningOnlyDelegate : public UsdUtilsCoalescingDiagnosticDelegate
{
    void IssueStatus(const TfStatus&) override { }
    void IssueFatalError(const TfCallContext&, const std::string&) override { }
};

} // anonymous namespace

static MString _FormatDiagnostic(const TfDiagnosticBase& d)
{
    if (!TfGetEnvSetting(MAYAUSD_SHOW_FULL_DIAGNOSTICS)) {
        return d.GetCommentary().c_str();
    } else {
        const std::string msg = TfStringPrintf(
            "%s -- %s in %s at line %zu of %s",
            d.GetCommentary().c_str(),
            TfDiagnosticMgr::GetCodeName(d.GetDiagnosticCode()).c_str(),
            d.GetContext().GetFunction(),
            d.GetContext().GetLine(),
            ghc::filesystem::path(d.GetContext().GetFile()).relative_path().string().c_str());
        return msg.c_str();
    }
}

static MString _FormatCoalescedDiagnostic(const UsdUtilsCoalescingDiagnosticDelegateItem& item)
{
    const size_t      numItems = item.unsharedItems.size();
    const std::string suffix
        = numItems == 1 ? std::string() : TfStringPrintf(" -- and %zu similar", numItems - 1);
    const std::string message
        = TfStringPrintf("%s%s", item.unsharedItems[0].commentary.c_str(), suffix.c_str());

    return message.c_str();
}

static bool _IsDiagnosticBatchingEnabled() { return TfGetEnvSetting(PIXMAYA_DIAGNOSTICS_BATCH); }

UsdMayaDiagnosticDelegate::UsdMayaDiagnosticDelegate()
    : _batchCount(0)
{
    TfDiagnosticMgr::GetInstance().AddDelegate(this);
}

UsdMayaDiagnosticDelegate::~UsdMayaDiagnosticDelegate()
{
    // If a batch context was open when the delegate is removed, we need to
    // flush all the batched diagnostics in order to avoid losing any.
    // The batch context should know how to clean itself up when the delegate
    // is gone.
    _FlushBatch();
    TfDiagnosticMgr::GetInstance().RemoveDelegate(this);
}

void UsdMayaDiagnosticDelegate::IssueError(const TfError& err)
{
    // Errors are never batched. They should be rare, and in those cases, we
    // want to see them separately.

    const auto diagnosticMessage = _FormatDiagnostic(err);

    if (ArchIsMainThread()) {
        MGlobal::displayError(diagnosticMessage);
    } else {
        std::cerr << diagnosticMessage << std::endl;
    }
}

void UsdMayaDiagnosticDelegate::IssueStatus(const TfStatus& status)
{
    if (_batchCount.load() > 0) {
        return; // Batched.
    }

    const auto diagnosticMessage = _FormatDiagnostic(status);

    if (ArchIsMainThread()) {
        MGlobal::displayInfo(diagnosticMessage);
    } else {
        std::cerr << diagnosticMessage << std::endl;
    }
}

void UsdMayaDiagnosticDelegate::IssueWarning(const TfWarning& warning)
{
    if (_batchCount.load() > 0) {
        return; // Batched.
    }

    const auto diagnosticMessage = _FormatDiagnostic(warning);

    if (ArchIsMainThread()) {
        MGlobal::displayWarning(diagnosticMessage);
    } else {
        std::cerr << diagnosticMessage << std::endl;
    }
}

void UsdMayaDiagnosticDelegate::IssueFatalError(
    const TfCallContext& context,
    const std::string&   msg)
{
    TfLogCrash(
        "FATAL ERROR",
        msg,
        /*additionalInfo*/ std::string(),
        context,
        /*logToDb*/ true);
    _UnhandledAbort();
}

/* static */
void UsdMayaDiagnosticDelegate::InstallDelegate()
{
    if (!ArchIsMainThread()) {
        TF_FATAL_CODING_ERROR("Cannot install delegate from secondary thread");
    }

    if (_installationCount++ > 0) {
        return;
    }

    _sharedDelegate.reset(new UsdMayaDiagnosticDelegate());
}

/* static */
void UsdMayaDiagnosticDelegate::RemoveDelegate()
{
    if (!ArchIsMainThread()) {
        TF_FATAL_CODING_ERROR("Cannot remove delegate from secondary thread");
    }

    if (_installationCount == 0 || _installationCount-- > 1) {
        return;
    }

    _sharedDelegate.reset();
}

/* static */
int UsdMayaDiagnosticDelegate::GetBatchCount()
{
    if (std::shared_ptr<UsdMayaDiagnosticDelegate> ptr = _sharedDelegate) {
        return ptr->_batchCount.load();
    }

    TF_RUNTIME_ERROR("Delegate is not installed");
    return 0;
}

void UsdMayaDiagnosticDelegate::_StartBatch()
{
    TF_AXIOM(ArchIsMainThread());

    if (_batchCount.fetch_add(1) == 0) {
        // This is the first _StartBatch; add the batching delegates.
        _batchedStatuses.reset(new _StatusOnlyDelegate());
        _batchedWarnings.reset(new _WarningOnlyDelegate());
    }
}

void UsdMayaDiagnosticDelegate::_EndBatch()
{
    TF_AXIOM(ArchIsMainThread());

    const int prevValue = _batchCount.fetch_sub(1);
    if (prevValue <= 0) {
        TF_FATAL_ERROR("_EndBatch invoked before _StartBatch");
    } else if (prevValue == 1) {
        // This is the last _EndBatch; print the diagnostic messages.
        // and remove the batching delegates.
        _FlushBatch();
        _batchedStatuses.reset();
        _batchedWarnings.reset();
    }
}

void UsdMayaDiagnosticDelegate::_FlushBatch()
{
    TF_AXIOM(ArchIsMainThread());

    const UsdUtilsCoalescingDiagnosticDelegateVector statuses = _batchedStatuses
        ? _batchedStatuses->TakeCoalescedDiagnostics()
        : UsdUtilsCoalescingDiagnosticDelegateVector();
    const UsdUtilsCoalescingDiagnosticDelegateVector warnings = _batchedWarnings
        ? _batchedWarnings->TakeCoalescedDiagnostics()
        : UsdUtilsCoalescingDiagnosticDelegateVector();

    // Note that we must be in the main thread here, so it's safe to call
    // displayInfo/displayWarning.
    for (const UsdUtilsCoalescingDiagnosticDelegateItem& item : statuses) {
        MGlobal::displayInfo(_FormatCoalescedDiagnostic(item));
    }
    for (const UsdUtilsCoalescingDiagnosticDelegateItem& item : warnings) {
        MGlobal::displayWarning(_FormatCoalescedDiagnostic(item));
    }
}

UsdMayaDiagnosticBatchContext::UsdMayaDiagnosticBatchContext()
    : _delegate(_IsDiagnosticBatchingEnabled() ? _sharedDelegate : nullptr)
{
    TF_DEBUG(PXRUSDMAYA_DIAGNOSTICS).Msg(">> Entering batch context\n");
    if (!ArchIsMainThread()) {
        TF_FATAL_CODING_ERROR("Cannot construct context on secondary thread");
    }
    if (std::shared_ptr<UsdMayaDiagnosticDelegate> ptr = _delegate.lock()) {
        ptr->_StartBatch();
    }
}

UsdMayaDiagnosticBatchContext::~UsdMayaDiagnosticBatchContext()
{
    TF_DEBUG(PXRUSDMAYA_DIAGNOSTICS).Msg("!! Exiting batch context\n");
    if (!ArchIsMainThread()) {
        TF_FATAL_CODING_ERROR("Cannot destruct context on secondary thread");
    }
    if (std::shared_ptr<UsdMayaDiagnosticDelegate> ptr = _delegate.lock()) {
        ptr->_EndBatch();
    }
}

PXR_NAMESPACE_CLOSE_SCOPE
