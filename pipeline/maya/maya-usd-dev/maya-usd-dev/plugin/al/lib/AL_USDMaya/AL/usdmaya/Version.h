//
// Copyright 2017 Animal Logic
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

#pragma once

#include <string>

#define xstr(a)      stringify(a)
#define stringify(a) #a

#define AL_USDMAYA_VERSION_MAJOR 3
#define AL_USDMAYA_VERSION_MINOR 0
#define AL_USDMAYA_VERSION_PATCH 0

#define AL_USDMAYA_VERSION_STR                                                  \
    xstr(AL_USDMAYA_VERSION_MAJOR) "." xstr(AL_USDMAYA_VERSION_MINOR) "." xstr( \
        AL_USDMAYA_VERSION_PATCH)

namespace AL {
namespace usdmaya {

inline const char* getVersion() { return AL_USDMAYA_VERSION_STR; }

} // namespace usdmaya
} // namespace AL
