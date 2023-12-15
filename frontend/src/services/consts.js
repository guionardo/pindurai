export function useConsts() {
    const Version = '0.1.0'
    const AppTitle = 'PindurAí'
    const BackendUrl = process.env.BACKEND_URL || '/'
    const StorageKey = 'pinduraiAuth'

    return { Version, AppTitle, BackendUrl, StorageKey }
}
