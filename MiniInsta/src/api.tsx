import { Platform } from "react-native";

export type Photo = {
  id: number;
  image: string;
};

export type Profile = {
  id: number;
  username: string;
  display_name: string;
  profile_image_url: string;
  bio_text: string;
  join_date: string;
  num_followers: number;
  num_following: number;
};

export type Post = {
  id: number;
  profile_id: number;
  caption: string;
  timestamp?: string;
  photos?: Photo[];
};

export type LoginResponse = {
  token: string;
  profile: Profile;
};

type RequestOptions = {
  method?: string;
  headers?: Record<string, string>;
  body?: string;
};

type CreatePostPayload = {
  caption: string;
  image_url: string;
};

const apiHost = Platform.select({
  ios: "http://127.0.0.1:8000",
  android: "http://10.0.2.2:8000",
  default: "http://127.0.0.1:8000",
});

const API_BASE = `${apiHost}/mini_insta/api`;

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
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

  return data as T;
}

export function apiLogin(username: string, password: string): Promise<LoginResponse> {
  return request<LoginResponse>("/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function apiGetMyProfile(token: string): Promise<Profile> {
  return request<Profile>("/me/", {
    headers: { Authorization: `Token ${token}` },
  });
}

export function apiGetMyPosts(token: string): Promise<Post[]> {
  return request<Post[]>("/me/posts/", {
    headers: { Authorization: `Token ${token}` },
  });
}

export function apiGetMyFeed(token: string): Promise<Post[]> {
  return request<Post[]>("/me/feed/", {
    headers: { Authorization: `Token ${token}` },
  });
}

export function apiCreatePost(token: string, payload: CreatePostPayload): Promise<Post> {
  return request<Post>("/posts/", {
    method: "POST",
    headers: { Authorization: `Token ${token}` },
    body: JSON.stringify(payload),
  });
}
