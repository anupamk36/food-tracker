const KEY = "ft_token";

export function saveToken(token) {
    try { localStorage.setItem(KEY, token); } catch { }
    return token;
}

export function getToken() {
    try { return localStorage.getItem(KEY); } catch { return null; }
}

export function clearToken() {
    try { localStorage.removeItem(KEY); } catch { }
}

export function isAuthed() {
    return !!getToken();
}
