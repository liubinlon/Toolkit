//Maya ASCII 2012 scene
//Name: bird.ma
//Last modified: Sat, May 23, 2015 10:36:28 AM
//Codeset: 1252
requires maya "2008";
fileInfo "application" "maya";
fileInfo "product" "Maya 2012";
fileInfo "version" "2012 x64";
fileInfo "cutIdentifier" "001200000000-796618";
fileInfo "osv" "Microsoft Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -3.9443977642451191 2.5613895653955456 4.834114549507694 ;
	setAttr ".r" -type "double3" -16.414922709178303 -33.799999999952384 9.5686345505326438e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".ncp" 1;
	setAttr ".coi" 6.5085303143671798;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -0.26535086366365945 0.50904242976851077 -0.24579281949600773 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -1.3929448783800233 129.8589772880953 -0.22062758700551544 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ncp" 1;
	setAttr ".coi" 100.1;
	setAttr ".ow" 7.338257345356066;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -2.8959614430915073 0.63474921383331995 129.40931629835288 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ncp" 1;
	setAttr ".coi" 100.1;
	setAttr ".ow" 11.004622939274235;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 101.31869478795808 1.3665175266530913 -0.078903496644691484 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
	setAttr ".rp" -type "double3" 0 0 -1.4210854715202004e-014 ;
	setAttr ".rpt" -type "double3" -1.4210854715202007e-014 0 1.4210854715202007e-014 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".ncp" 1;
	setAttr ".coi" 103.38306011569091;
	setAttr ".ow" 3.143568032087285;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".tp" -type "double3" -2.0643653277328298 0.60732651317330688 -0.29992965959537815 ;
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "FitSkeleton";
	addAttr -ci true -sn "visCylinders" -ln "visCylinders" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "visBoxes" -ln "visBoxes" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "visBones" -ln "visBones" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "lockCenterJoints" -ln "lockCenterJoints" -dv 1 -min 0 -max 
		1 -at "bool";
	addAttr -ci true -sn "visGap" -ln "visGap" -dv 0.75 -min 0 -max 1 -at "double";
	setAttr ".ove" yes;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".visBoxes" yes;
	setAttr ".visGap" 1;
createNode nurbsCurve -n "FitSkeletonShape" -p "FitSkeleton";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 29;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		0.78778975261213091 4.8238209946876527e-017 -0.78778975261212947
		-1.2710582550070557e-016 6.8219130731473504e-017 -1.1141029524426198
		-0.78778975261213002 4.823820994687657e-017 -0.78778975261213002
		-1.1141029524426198 3.3774088972751678e-033 -2.7568967384780713e-017
		-0.78778975261213002 -4.8238209946876527e-017 0.78778975261212947
		-3.3570096253603121e-016 -6.8219130731473516e-017 1.1141029524426205
		0.78778975261212947 -4.823820994687657e-017 0.78778975261213002
		1.1141029524426198 -5.3031416674093278e-032 8.9365706465388486e-016
		0.78778975261213091 4.8238209946876527e-017 -0.78778975261212947
		-1.2710582550070557e-016 6.8219130731473504e-017 -1.1141029524426198
		-0.78778975261213002 4.823820994687657e-017 -0.78778975261213002
		;
createNode joint -n "Root" -p "FitSkeleton";
	addAttr -ci true -sn "run" -ln "run" -dt "string";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.25744699893917217 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	addAttr -ci true -k true -sn "centerBtwFeet" -ln "centerBtwFeet" -min 0 -max 1 -at "bool" -dv true;
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0 1.0580263833117491 -0.37006808183555928 ;
	setAttr -l on ".tx";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".ro" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 89.999999999999915 -61.03888329028937 90.000000000000114 ;
	setAttr ".dl" yes;
	setAttr ".typ" 1;
	setAttr -k on ".run";
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.2574470043182373;
	setAttr ".fatZabs" 0.2574470043182373;
createNode joint -n "Hip" -p "Root";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.32656086305614013 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" -0.047271778107423418 0.42179704303446752 -0.21785485979860483 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 146.9862393333583 ;
	setAttr ".dl" yes;
	setAttr ".typ" 2;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Knee" -p "Hip";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.33131609538367984 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.32656086305614684 -6.3282712403633923e-015 -7.1331829332166308e-015 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -47.743939763203905 ;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Ankle" -p "Knee";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.037357417561876632 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	addAttr -ci true -k true -sn "worldOrient" -ln "worldOrient" -min 0 -max 5 -en "xUp:yUp:zUp:xDown:yDown:zDown" 
		-at "enum";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.33131609538367923 -1.1102230246251565e-015 1.5015766408055242e-014 ;
	setAttr ".ro" 3;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.019148421094928682 0 19.718817139556251 ;
	setAttr ".pa" -type "double3" 3.1147589914174403 -1.2104724556304993 -11.405913270501992 ;
	setAttr ".dl" yes;
	setAttr ".typ" 4;
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.03735741600394249;
	setAttr ".fatZabs" 0.03735741600394249;
	setAttr -k on ".worldOrient" 3;
createNode joint -n "Heel" -p "Ankle";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.037357417561876632 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.065233458670876543 0.015702747938421524 4.6906922790412864e-015 ;
	setAttr ".r" -type "double3" 0 -2.055155944776297e-022 7.3775844857871918e-031 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.019136588808166714 -2.159915354754721 -3.4277916334574723 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Heel";
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
createNode joint -n "Toes" -p "Ankle";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.32268411320534407 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.037175409455805497 -0.034223873633514867 -1.1879386363489175e-014 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.5373245161612658e-005 3.8031121366765598e-005 -85.015929172674717 ;
	setAttr ".pa" -type "double3" -0.00019030234564052423 0.00053514845282692043 25.864574245063647 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Toes";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 0.1;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.010000000707805157;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "ToesEnd" -p "Toes";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.32268411320534407 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.32268411320534468 1.4259426972529354e-015 -3.1607945150113892e-009 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -3.4066436846343579e-005 0 0 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "ToesEnd";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 0.1;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.010000000707805157;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Tail1" -p "Root";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.45688826117041126 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	addAttr -ci true -k true -sn "flipOrient" -ln "flipOrient" -dv 1 -min 0 -max 1 -at "bool";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" -0.33827292612530019 -0.032802003759444975 -3.9779143460537632e-017 ;
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" -4.0325598525573692e-013 -1.9984347314917702e-015 -8.1422199845466029e-013 ;
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 180 2.6067108317879821 ;
	setAttr ".radi" 0.92091889086594292;
	setAttr -k on ".fat" 0.23688826117041123;
	setAttr -k on ".fatY" 0.6399999999999999;
	setAttr -k on ".fatZ" 1.7800000000000002;
	setAttr ".fatYabs" 0.15160848200321198;
	setAttr ".fatZabs" 0.42166110873222351;
createNode joint -n "Tail2" -p "Tail1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.17086755573921963 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.45688826117040848 -5.773159728050814e-015 1.5935927171130261e-017 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".radi" 0.92971683133986383;
	setAttr -k on ".fat";
	setAttr -k on ".fatY" 0.6399999999999999;
	setAttr -k on ".fatZ" 1.7800000000000002;
	setAttr ".fatYabs" 0.10935524106025696;
	setAttr ".fatZabs" 0.30414426326751709;
createNode joint -n "Tail3ASide" -p "Tail2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.58321337216002278 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.17086755573921986 -0.002519829184515654 0.81755406230483774 ;
	setAttr ".r" -type "double3" 1.1032549051326891e-014 7.7526020360673172e-014 4.6913181551586868e-013 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -13.395523038792755 -26.397871835987004 0.27637048550497717 ;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 0.1;
	setAttr -k on ".fatZ" 1.7000000000000002;
	setAttr ".fatYabs" 0.010000000707805157;
	setAttr ".fatZabs" 0.17000000178813934;
createNode joint -n "Tail3Side" -p "Tail3ASide";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.14999999999999991 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.58321337216002811 4.8849813083506888e-015 -9.9920072216264089e-016 ;
	setAttr ".r" -type "double3" 5.9820544422467586e-014 1.1227358025566215e-012 -3.3925916602279116e-013 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 20.000000000000053 0 ;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 0.1;
	setAttr -k on ".fatZ" 1.7000000000000002;
	setAttr ".fatYabs" 0.010000000707805157;
	setAttr ".fatZabs" 0.17000000178813934;
createNode joint -n "Tail3SideEnd" -p "Tail3Side";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.14999999999999991 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.14999999999999281 -1.1102230246251565e-015 -2.4424906541753444e-015 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 0.1;
	setAttr -k on ".fatZ" 1.7000000000000002;
	setAttr ".fatYabs" 0.010000000707805157;
	setAttr ".fatZabs" 0.17000000178813934;
createNode joint -n "Tail3" -p "Tail2";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.14999999999999902 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.95839271293790496 -1.3322676295501878e-015 -4.1141589008308129e-016 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".fat";
	setAttr -k on ".fatY" 0.6399999999999999;
	setAttr -k on ".fatZ" 1.7800000000000002;
	setAttr ".fatYabs" 0.096000000834465027;
	setAttr ".fatZabs" 0.26700001955032349;
createNode joint -n "Tail3End" -p "Tail3";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.14999999999999902 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.15000000000000235 -1.7763568394002505e-015 2.3601591879817414e-017 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".fat";
	setAttr -k on ".fatY" 0.6399999999999999;
	setAttr -k on ".fatZ" 1.7800000000000002;
	setAttr ".fatYabs" 0.096000000834465027;
	setAttr ".fatZabs" 0.26700001955032349;
createNode joint -n "Spine1" -p "Root";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.29911800073071737 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.25744699893917217 -4.4408920985006262e-016 1.9750923112209416e-016 ;
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" -3.5912614642346691e-017 2.2540796298639536e-015 1.9560411291000627e-013 ;
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -1.8255496810888925 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Mid";
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.29911801218986511;
	setAttr ".fatZabs" 0.29911801218986511;
createNode joint -n "Chest" -p "Spine1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.23098434682418767 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.29911800073071743 1.3322676295501878e-015 -1.1767634511696997e-017 ;
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" 6.4309185718152102e-015 -5.2149882758926511e-014 1.3835412864366299e-013 ;
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -14.059997956784398 ;
	setAttr ".dl" yes;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Chest";
	setAttr -k on ".fat" 0.30098434682418773;
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.30098435282707214;
	setAttr ".fatZabs" 0.30098435282707214;
createNode joint -n "Scapula" -p "Chest";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.16434865912560742 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.23098434682418545 -0.092918807029922168 -0.39457371274715392 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.54980958966874 89.999998627800721 104.90443312346797 ;
	setAttr ".otp" -type "string" "PropA1";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 2.9000000000000004;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.29000002145767212;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Shoulder" -p "Scapula";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.64310293807879848 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.1643486591256052 -6.4392935428259079e-015 -4.4408920985006262e-016 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -15.000000000000046 ;
	setAttr ".pa" -type "double3" -4.1293130717023516e-007 0 0 ;
	setAttr ".typ" 10;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 2.9000000000000004;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.29000002145767212;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Elbow" -p "Shoulder";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.97953586154532313 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.64310293807880137 3.3306690738754696e-016 -1.5543122344752192e-015 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 24.999999999999996 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "22";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 2.9000000000000004;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.29000002145767212;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Wrist" -p "Elbow";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.58385734483332996 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.97953586154532934 -1.6653345369377348e-016 1.1791467802169109e-009 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -15.000000000000002 ;
	setAttr ".typ" 12;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 2.9000000000000004;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.29000002145767212;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "IndexFinger1" -p "Wrist";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.43819887037736649 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.58385734483332863 4.4408920985006262e-016 1.9127497363768953e-009 ;
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 14.999999999999996 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "8";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 2.1000000000000005;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.20999999344348907;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "IndexFinger2" -p "IndexFinger1";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.43819887037736649 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.43819887037736205 2.2204460492503131e-016 9.2676044616268882e-010 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY" 2;
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.20000000298023224;
	setAttr ".fatZabs" 0.10000000149011612;
createNode joint -n "Neck" -p "Chest";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.32607764456711119 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.45195534111228297 1.2212453270876722e-015 4.1136394777375527e-016 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -13.22716042720797 ;
	setAttr ".pa" -type "double3" -1.7940447748746266e-016 6.8425179703803005e-015 0 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "37";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 1;
	setAttr ".fatZabs" 1;
createNode joint -n "Head" -p "Neck";
	addAttr -ci true -k true -sn "global" -ln "global" -min 0 -max 10 -at "long";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.2 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.32607764456710964 4.4408920985006262e-016 2.2046054276185068e-016 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".ro" 5;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -31.926175225208095 ;
	setAttr ".otp" -type "string" "36";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 1;
	setAttr ".fatZabs" 1;
createNode joint -n "Eye" -p "Head";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.065788011694844939 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	addAttr -ci true -k true -sn "noFlip" -ln "noFlip" -dv 1 -min 0 -max 1 -at "bool";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.089354900367531798 0.18920836869073876 -0.15028813426131357 ;
	setAttr ".ro" 2;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 4.946743 63.402557530707796 95.528753825917036 ;
	setAttr ".pa" -type "double3" 8.9959671327899885e-014 -89.999999999998849 0 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "Eye";
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
createNode joint -n "EyeEnd" -p "Eye";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.065788011694844939 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.085788011694844124 1.3322676295501878e-015 6.6613381477509392e-016 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 89.999999999999815 0 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "24";
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
createNode joint -n "Jaw" -p "Head";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" -0.061692624887422776 0.17275930072084966 -4.5969931233202043e-017 ;
	setAttr -l on ".tz";
	setAttr ".r" -type "double3" 2.6102766841419818e-014 2.3730001138963595e-014 -2.0355549961366507e-013 ;
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 95.452109783142873 ;
	setAttr ".otp" -type "string" "31";
	setAttr ".radi" 0.5;
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
createNode joint -n "JawEnd" -p "Jaw";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.05 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".ove" yes;
	setAttr ".t" -type "double3" 0.30100228190598477 -1.1102230246251565e-015 -1.2466510715381254e-016 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "25";
	setAttr -k on ".fat";
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
createNode joint -n "HeadEnd" -p "Head";
	addAttr -ci true -k true -sn "fat" -ln "fat" -dv 0.2 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatY" -ln "fatY" -dv 1 -min 0 -at "double";
	addAttr -ci true -k true -sn "fatZ" -ln "fatZ" -dv 1 -min 0 -at "double";
	addAttr -ci true -sn "fatYabs" -ln "fatYabs" -at "double";
	addAttr -ci true -sn "fatZabs" -ln "fatZabs" -at "double";
	setAttr ".t" -type "double3" 0.30000000000000249 2.2204460492503131e-016 -3.3526588471893002e-030 ;
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".typ" 18;
	setAttr ".otp" -type "string" "23";
	setAttr -k on ".fat" 0.1;
	setAttr -k on ".fatY";
	setAttr -k on ".fatZ";
	setAttr ".fatYabs" 0.10000000149011612;
	setAttr ".fatZabs" 0.10000000149011612;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 11 ".lnk";
	setAttr -s 11 ".slnk";
createNode displayLayerManager -n "layerManager";
	setAttr ".cdl" 2;
	setAttr -s 3 ".dli[1:2]"  1 2;

connectAttr "Root.s" "Hip.is";
connectAttr "Hip.s" "Knee.is";
connectAttr "Knee.s" "Ankle.is";
connectAttr "Ankle.s" "Heel.is";
connectAttr "Ankle.s" "Toes.is";
connectAttr "Toes.s" "ToesEnd.is";
connectAttr "Root.s" "Tail1.is";
connectAttr "Tail1.s" "Tail2.is";
connectAttr "Tail2.s" "Tail3ASide.is";
connectAttr "Tail3ASide.s" "Tail3Side.is";
connectAttr "Tail3Side.s" "Tail3SideEnd.is";
connectAttr "Tail2.s" "Tail3.is";
connectAttr "Tail3.s" "Tail3End.is";
connectAttr "Root.s" "Spine1.is";
connectAttr "Spine1.s" "Chest.is";
connectAttr "Chest.s" "Scapula.is";
connectAttr "Scapula.s" "Shoulder.is";
connectAttr "Shoulder.s" "Elbow.is";
connectAttr "Elbow.s" "Wrist.is";
connectAttr "Wrist.s" "IndexFinger1.is";
connectAttr "IndexFinger1.s" "IndexFinger2.is";
connectAttr "Chest.s" "Neck.is";
connectAttr "Neck.s" "Head.is";
connectAttr "Head.s" "Eye.is";
connectAttr "Eye.s" "EyeEnd.is";
connectAttr "Head.s" "Jaw.is";
connectAttr "Jaw.s" "JawEnd.is";
connectAttr "Head.s" "HeadEnd.is";

// End of bird.ma
