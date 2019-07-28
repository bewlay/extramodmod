#include "CvGameCoreDLL.h"
#include "CvUniversalPrereqs.h"

// UNIVERSAL_PREREQS 07/2019 lfgr
// Python interface for CvPrereqStruct

void CyUniveralPrereqsPythonInterface()
{
	OutputDebugString("Python Extension Module - CyUniveralPrereqsPythonInterface\n");

	python::class_<CvPrereqStruct>("CvPrereqStruct")
		.def("getIntValue", &CvPrereqStruct::getIntValue, "int ()")
		.def("getStringValue", &CvPrereqStruct::getStringValue, "str ()")
		.def("getName", &CvPrereqStruct::getName, "str ()")
		.def("getNumChildren", &CvPrereqStruct::getNumChildren, "str ()")
		.def("getChild", &CvPrereqStruct::getChild,
				python::return_value_policy<python::reference_existing_object>(),
				"CvPrereqStruct ( int idx )")
		;
}
