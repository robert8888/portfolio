export const getResponseFilename = (response: Response): string => {
    const value = response.headers.get('Content-Disposition')
    const regex = /filename=(?<filename>.*)$/
    return value?.match(regex)?.groups?.filename || ''
}