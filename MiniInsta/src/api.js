import { Platform } from "react-native";

const apiHost = Platform.select({
  ios: "http://127.0.0.1:8000",
  android: "http://10.0.2.2:8000",
  default: "http://127.0.0.1:8000",
});

const API_BASE = `${apiHost}/mini_insta/api`;

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const text = await response.text();
  const data = text ? JSON.parse(text) : {};

  if (!response.ok) {
    const message = data.detail || data.non_field_errors?.[0] || "Request failed";
    throw new Error(message);
  }

  return data;
}

export function apiLogin(username, password) {
  return request("/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function apiGetMyProfile(token) {
  return request("/me/", {
    headers: { Authorization: `Token ${token}` },
  });
}

export function apiGetMyPosts(token) {
  return request("/me/posts/", {
    headers: { Authorization: `Token ${token}` },
  });
}

export function apiGetMyFeed(token) {
  return request("/me/feed/", {
    headers: { Authorization: `Token ${token}` },
  });
}

export function apiCreatePost(token, payload) {
  return request("/posts/", {
    method: "POST",
    headers: { Authorization: `Token ${token}` },
    body: JSON.stringify(payload),
  });
}
