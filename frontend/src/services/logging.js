const DEBUG = true
const logInfo = (message, any) => console.info(message, any)
const logDebug = (message, any) => DEBUG ? console.debug(message, any) : null
const logError = (message, any) => console.error(message, any)
