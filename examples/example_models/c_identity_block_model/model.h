
// CIdentityBlock/model.h
#ifndef MODEL_H
#define MODEL_H

#include <stddef.h> // For size_t
#include <stdbool.h> // For bool

// Define FMI 2.0 data types for clarity
typedef void* fmi2Component;
typedef void* fmi2ComponentEnvironment;
typedef unsigned int fmi2ValueReference;
typedef double fmi2Real;
typedef int fmi2Integer;
typedef int fmi2Boolean;
typedef const char* fmi2String;
typedef unsigned char fmi2Byte;
typedef int fmi2Status;

// FMI 2.0 Status codes
#define fmi2OK       0
#define fmi2Warning  1
#define fmi2Discard  2
#define fmi2Error    3
#define fmi2Fatal    4
#define fmi2Pending  5

// FMI 2.0 Boolean values
#define fmi2True  1
#define fmi2False 0

// Function prototypes for the FMI 2.0 Co-simulation interface

// Common Functions (Inquiry and Debugging)
fmi2String fmi2GetTypesPlatform();
fmi2String fmi2GetVersion();
fmi2Status fmi2SetDebugLogging(fmi2Component c, fmi2Boolean loggingOn, size_t nCategories, const fmi2String categories[]);

// Common Functions (Instance Life Cycle)
fmi2Component fmi2Instantiate(
    fmi2String instanceName,
    int fmuType, // fmi2CoSimulation or fmi2ModelExchange
    fmi2String fmuGUID,
    fmi2String fmuResourceLocation,
    const void* functions, // fmi2CallbackFunctions*
    fmi2Boolean visible,
    fmi2Boolean loggingOn
);
fmi2Status fmi2SetupExperiment(
    fmi2Component c,
    fmi2Boolean toleranceDefined,
    fmi2Real tolerance,
    fmi2Real startTime,
    fmi2Boolean stopTimeDefined,
    fmi2Real stopTime
);
fmi2Status fmi2EnterInitializationMode(fmi2Component c);
fmi2Status fmi2ExitInitializationMode(fmi2Component c);
fmi2Status fmi2Terminate(fmi2Component c);
fmi2Status fmi2Reset(fmi2Component c);
void fmi2FreeInstance(fmi2Component c);

// Common Functions (Getting/Setting Variable Values)
fmi2Status fmi2GetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]);
fmi2Status fmi2SetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]);
fmi2Status fmi2GetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]);
fmi2Status fmi2SetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]);
fmi2Status fmi2GetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]);
fmi2Status fmi2SetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]);
fmi2Status fmi2GetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]);
fmi2Status fmi2SetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]);
fmi2Status fmi2SetRealInputDerivatives(
    fmi2Component c,
    const fmi2ValueReference vr[],
    size_t nvr,
    const fmi2Integer order[],
    const fmi2Real value[]
);
fmi2Status fmi2GetRealOutputDerivatives(
    fmi2Component c,
    const fmi2ValueReference vr[],
    size_t nvr,
    const fmi2Integer order[],
    fmi2Real value[]
);

// Common Functions (FMU State Management)
fmi2Status fmi2GetFMUstate(fmi2Component c, fmi2Byte** FMUstate);
fmi2Status fmi2SetFMUstate(fmi2Component c, fmi2Byte* FMUstate);
fmi2Status fmi2FreeFMUstate(fmi2Component c, fmi2Byte** FMUstate);
fmi2Status fmi2SerializedFMUstateSize(fmi2Component c, size_t* size);
fmi2Status fmi2SerializeFMUstate(fmi2Component c, fmi2Byte serializedState[], size_t size, size_t* serializedSize);
fmi2Status fmi2DeSerializeFMUstate(fmi2Component c, const fmi2Byte serializedState[], size_t size, fmi2Byte** FMUstate);

// Common Functions (Directional Derivatives)
fmi2Status fmi2GetDirectionalDerivative(
    fmi2Component c,
    const fmi2ValueReference vUnknownRef[],
    size_t nUnknown,
    const fmi2ValueReference vKnownRef[],
    size_t nKnown,
    const fmi2Real dvKnown[],
    fmi2Real dvUnknown[]
);

// Co-simulation specific functions
fmi2Status fmi2CancelStep(fmi2Component c);
fmi2Status fmi2DoStep(
    fmi2Component c,
    fmi2Real currentCommunicationPoint,
    fmi2Real communicationStepSize,
    fmi2Boolean newDiscreteStatesNeeded
);

// Optional: fmi2GetStatus (for general status queries)
fmi2Status fmi2GetStatus(fmi2Component c, int statusKind, fmi2Status* value);

// Status Query Functions
fmi2Status fmi2GetRealStatus(fmi2Component c, int statusKind, fmi2Real* value);
fmi2Status fmi2GetIntegerStatus(fmi2Component c, int statusKind, fmi2Integer* value);
fmi2Status fmi2GetBooleanStatus(fmi2Component c, int statusKind, fmi2Boolean* value);
fmi2Status fmi2GetStringStatus(fmi2Component c, int statusKind, fmi2String* value);

#endif // MODEL_H
