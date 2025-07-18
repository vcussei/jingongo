
// CIdentityBlock/model.c
#include "model.h"
#include <stdio.h> // For printf, snprintf
#include <stdlib.h> // For malloc, free
#include <string.h> // For memcpy

// Define value references for our variables
#define VR_TEST_PARAM   0
#define VR_INPUT_VALUE   1
#define VR_OUTPUT_VALUE  2

// Simple struct to hold instance data
typedef struct {
    fmi2ComponentEnvironment componentEnvironment;
    fmi2String instanceName;
    fmi2Real test_param;
    fmi2Real input_value;
    fmi2Real output_value;
    bool loggingOn;
} ModelInstance;

static void logMessage(fmi2ComponentEnvironment componentEnvironment, fmi2String instanceName, fmi2Status status, fmi2String category, fmi2String message) {
    if (status >= fmi2Warning) {
        fprintf(stderr, "[FMI Log] %s (%s) [%d]: %s\n", instanceName, category, status, message);
    } else {
        printf("[FMI Log] %s (%s): %s\n", instanceName, category, message);
    }
}

fmi2String fmi2GetTypesPlatform() { return "default"; }
fmi2String fmi2GetVersion() { return "2.0"; }
fmi2Status fmi2SetDebugLogging(fmi2Component c, fmi2Boolean loggingOn, size_t nCategories, const fmi2String categories[]) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    instance->loggingOn = (bool)loggingOn;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2SetDebugLogging called."); }
    return fmi2OK;
}

fmi2Component fmi2Instantiate( fmi2String instanceName, int fmuType, fmi2String fmuGUID, fmi2String fmuResourceLocation, const void* functions, fmi2Boolean visible, fmi2Boolean loggingOn ) {
    ModelInstance* instance = (ModelInstance*)malloc(sizeof(ModelInstance));
    if (!instance) { return NULL; }
    instance->componentEnvironment = NULL;
    instance->instanceName = instanceName;
    instance->test_param = 20.0;
    instance->input_value = 0.0;
    instance->output_value = 0.0;
    instance->loggingOn = (bool)loggingOn;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2Instantiate called."); }
    return (fmi2Component)instance;
}
fmi2Status fmi2SetupExperiment( fmi2Component c, fmi2Boolean toleranceDefined, fmi2Real tolerance, fmi2Real startTime, fmi2Boolean stopTimeDefined, fmi2Real stopTime ) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2SetupExperiment called."); }
    return fmi2OK;
}
fmi2Status fmi2EnterInitializationMode(fmi2Component c) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2EnterInitializationMode called."); }
    return fmi2OK;
}
fmi2Status fmi2ExitInitializationMode(fmi2Component c) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2ExitInitializationMode called."); }
    return fmi2OK;
}
fmi2Status fmi2Terminate(fmi2Component c) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2Terminate called."); }
    return fmi2OK;
}
fmi2Status fmi2Reset(fmi2Component c) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2Reset called."); }
    instance->test_param = 20.0;
    instance->input_value = 0.0;
    instance->output_value = 0.0;
    return fmi2OK;
}
void fmi2FreeInstance(fmi2Component c) {
    ModelInstance* instance = (ModelInstance*)c;
    if (instance) {
        if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2FreeInstance called."); }
        free(instance);
    }
}
fmi2Status fmi2GetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    for (size_t i = 0; i < nvr; i++) {
        if (0) { /* dummy for else if chain */ }
        else if (vr[i] == VR_TEST_PARAM) { value[i] = instance->test_param; }        else if (vr[i] == VR_INPUT_VALUE) { value[i] = instance->input_value; }        else if (vr[i] == VR_OUTPUT_VALUE) { value[i] = instance->output_value; }
        else { return fmi2Error; }
    }
    return fmi2OK;
}
fmi2Status fmi2SetReal(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    for (size_t i = 0; i < nvr; i++) {
        if (0) { /* dummy for else if chain */ }
        else if (vr[i] == VR_TEST_PARAM) { instance->test_param = value[i]; }        else if (vr[i] == VR_INPUT_VALUE) { instance->input_value = value[i]; }        // Output variable output_value cannot be set directly via fmi2SetReal
        else { return fmi2Error; }
    }
    return fmi2OK;
}
fmi2Status fmi2GetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) { return fmi2Error; }
fmi2Status fmi2SetInteger(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) { return fmi2Error; }
fmi2Status fmi2GetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) { return fmi2Error; }
fmi2Status fmi2SetBoolean(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]) { return fmi2Error; }
fmi2Status fmi2GetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) { return fmi2Error; }
fmi2Status fmi2SetString(fmi2Component c, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) { return fmi2Error; }

fmi2Status fmi2SetRealInputDerivatives(
    fmi2Component c,
    const fmi2ValueReference vr[],
    size_t nvr,
    const fmi2Integer order[],
    const fmi2Real value[]
) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;

    if (instance->loggingOn) {
        logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2SetRealInputDerivatives called (stub).");
    }
    return fmi2OK;
}

fmi2Status fmi2GetFMUstate(fmi2Component c, fmi2Byte** FMUstate) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    size_t state_size = sizeof(fmi2Real) * 3;
    fmi2Byte* state_bytes = (fmi2Byte*)malloc(state_size);
    if (!state_bytes) return fmi2Error;
    
    memcpy(state_bytes + 0, &instance->test_param, sizeof(fmi2Real));
    memcpy(state_bytes + 8, &instance->input_value, sizeof(fmi2Real));
    memcpy(state_bytes + 16, &instance->output_value, sizeof(fmi2Real));

    *FMUstate = state_bytes;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2GetFMUstate called."); }
    return fmi2OK;
}
fmi2Status fmi2SetFMUstate(fmi2Component c, fmi2Byte* FMUstate) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !FMUstate) return fmi2Error;
    
    memcpy(&instance->test_param, FMUstate + 0, sizeof(fmi2Real));
    memcpy(&instance->input_value, FMUstate + 8, sizeof(fmi2Real));
    memcpy(&instance->output_value, FMUstate + 16, sizeof(fmi2Real));

    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2SetFMUstate called."); }
    return fmi2OK;
}
fmi2Status fmi2FreeFMUstate(fmi2Component c, fmi2Byte** FMUstate) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !FMUstate || !*FMUstate) return fmi2Error;
    free(*FMUstate);
    *FMUstate = NULL;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2FreeInstance called."); }
    return fmi2OK;
}
fmi2Status fmi2SerializedFMUstateSize(fmi2Component c, size_t* size) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !size) return fmi2Error;
    *size = sizeof(fmi2Real) * 3;
    if (instance->loggingOn) {
        char msg_buffer[128];
        snprintf(msg_buffer, sizeof(msg_buffer), "fmi2SerializedFMUstateSize called. Size: %zu", *size);
        logMessage(NULL, instance->instanceName, fmi2OK, "log", msg_buffer);
    }
    return fmi2OK;
}
fmi2Status fmi2SerializeFMUstate(fmi2Component c, fmi2Byte serializedState[], size_t size, size_t* serializedSize) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !serializedState || !serializedSize) return fmi2Error;
    size_t required_size = sizeof(fmi2Real) * 3;
    *serializedSize = required_size;
    if (size < required_size) { return fmi2Discard; }
    
    memcpy(serializedState + 0, &instance->test_param, sizeof(fmi2Real));
    memcpy(serializedState + 8, &instance->input_value, sizeof(fmi2Real));
    memcpy(serializedState + 16, &instance->output_value, sizeof(fmi2Real));

    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2SerializeFMUstate called."); }
    return fmi2OK;
}
fmi2Status fmi2DeSerializeFMUstate(fmi2Component c, const fmi2Byte serializedState[], size_t size, fmi2Byte** FMUstate) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !serializedState || !FMUstate) return fmi2Error;
    size_t expected_size = sizeof(fmi2Real) * 3;
    if (size < expected_size) { return fmi2Error; }
    fmi2Byte* state_bytes = (fmi2Byte*)malloc(expected_size);
    if (!state_bytes) return fmi2Error;
    memcpy(state_bytes, serializedState, expected_size);
    
    memcpy(&instance->test_param, state_bytes + 0, sizeof(fmi2Real));
    memcpy(&instance->input_value, state_bytes + 8, sizeof(fmi2Real));
    memcpy(&instance->output_value, state_bytes + 16, sizeof(fmi2Real));

    *FMUstate = state_bytes;
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2DeSerializeFMUstate called."); }
    return fmi2OK;
}

fmi2Status fmi2GetDirectionalDerivative(
    fmi2Component c,
    const fmi2ValueReference vUnknownRef[],
    size_t nUnknown,
    const fmi2ValueReference vKnownRef[],
    size_t nKnown,
    const fmi2Real dvKnown[],
    fmi2Real dvUnknown[]
) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;

    if (instance->loggingOn) {
        logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2GetDirectionalDerivative called.");
    }

    for (size_t i = 0; i < nUnknown; ++i) {
        dvUnknown[i] = 0.0; // Initialize to zero
        for (size_t j = 0; j < nKnown; ++j) {
            // Assuming output_value is the only unknown that depends on input_value
            if (vUnknownRef[i] == VR_OUTPUT_VALUE && vKnownRef[j] == VR_INPUT_VALUE) {
                dvUnknown[i] += 1.0 * dvKnown[j]; // d(output_value)/d(input_value) = 1
            }
        }
    }
    return fmi2OK;
}

fmi2Status fmi2GetRealOutputDerivatives(
    fmi2Component c,
    const fmi2ValueReference vr[],
    size_t nvr,
    const fmi2Integer order[],
    fmi2Real value[]
) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;

    if (instance->loggingOn) {
        logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2GetRealOutputDerivatives called (stub).");
    }

    for (size_t i = 0; i < nvr; ++i) {
        value[i] = 0.0; // No inherent derivatives for this simple model
    }
    return fmi2OK;
}

fmi2Status fmi2CancelStep(fmi2Component c) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;

    if (instance->loggingOn) {
        logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2CancelStep called (stub).");
    }
    return fmi2OK;
}

fmi2Status fmi2DoStep( fmi2Component c, fmi2Real currentCommunicationPoint, fmi2Real communicationStepSize, fmi2Boolean newDiscreteStatesNeeded ) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance) return fmi2Error;
    
    // Core logic for the Identity Block
        instance->output_value = instance->input_value;

    if (instance->loggingOn) { printf("C Identity Block at time %.2f: Input = %.2f, Output = %.2f, TestParam = %.2f\n", currentCommunicationPoint, instance->input_value, instance->output_value, instance->test_param); }
    return fmi2OK;
}

fmi2Status fmi2GetStatus(fmi2Component c, int statusKind, fmi2Status* value) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !value) return fmi2Error;
    *value = fmi2OK; // Default to OK for a simple model
    if (instance->loggingOn) { logMessage(NULL, instance->instanceName, fmi2OK, "log", "fmi2GetStatus called."); }
    return fmi2OK;
}

fmi2Status fmi2GetRealStatus(fmi2Component c, int statusKind, fmi2Real* value) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !value) return fmi2Error;
    *value = 0.0; // Default value for a simple model
    if (instance->loggingOn) {
        char msg_buffer[128];
        snprintf(msg_buffer, sizeof(msg_buffer), "fmi2GetRealStatus called. Kind: %d", statusKind);
        logMessage(NULL, instance->instanceName, fmi2OK, "log", msg_buffer);
    }
    return fmi2OK;
}

fmi2Status fmi2GetIntegerStatus(fmi2Component c, int statusKind, fmi2Integer* value) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !value) return fmi2Error;
    *value = 0; // Default value for a simple model
    if (instance->loggingOn) {
        char msg_buffer[128];
        snprintf(msg_buffer, sizeof(msg_buffer), "fmi2GetIntegerStatus called. Kind: %d", statusKind);
        logMessage(NULL, instance->instanceName, fmi2OK, "log", msg_buffer);
    }
    return fmi2OK;
}

fmi2Status fmi2GetBooleanStatus(fmi2Component c, int statusKind, fmi2Boolean* value) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !value) return fmi2Error;
    *value = fmi2False; // Default value for a simple model
    if (instance->loggingOn) {
        char msg_buffer[128];
        snprintf(msg_buffer, sizeof(msg_buffer), "fmi2GetBooleanStatus called. Kind: %d", statusKind);
        logMessage(NULL, instance->instanceName, fmi2OK, "log", msg_buffer);
    }
    return fmi2OK;
}

fmi2Status fmi2GetStringStatus(fmi2Component c, int statusKind, fmi2String* value) {
    ModelInstance* instance = (ModelInstance*)c;
    if (!instance || !value) return fmi2Error;
    *value = ""; // Default empty string for a simple model
    if (instance->loggingOn) {
        char msg_buffer[128];
        snprintf(msg_buffer, sizeof(msg_buffer), "fmi2GetStringStatus called. Kind: %d", statusKind);
        logMessage(NULL, instance->instanceName, fmi2OK, "log", msg_buffer);
    }
    return fmi2OK;
}
