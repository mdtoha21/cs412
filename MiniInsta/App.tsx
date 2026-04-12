import AsyncStorage from "@react-native-async-storage/async-storage";
import { LinearGradient } from "expo-linear-gradient";
import React, { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Animated,
  Image,
  Pressable,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";

import {
  type LoginResponse,
  type Post,
  type Profile,
  apiCreatePost,
  apiGetMyFeed,
  apiGetMyPosts,
  apiGetMyProfile,
  apiLogin,
} from "./src/api";

const TOKEN_KEY = "mini_insta_token";
const PROFILE_ID_KEY = "mini_insta_profile_id";

export default function App(): React.JSX.Element {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [token, setToken] = useState<string | null>(null);
  const [profileId, setProfileId] = useState<number | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);
  const [feed, setFeed] = useState<Post[]>([]);
  const [caption, setCaption] = useState<string>("");
  const [imageUrl, setImageUrl] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [refreshing, setRefreshing] = useState<boolean>(false);

  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    void bootstrap();
  }, []);

  useEffect(() => {
    if (token) {
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 700,
        useNativeDriver: true,
      }).start();
    }
  }, [token, fadeAnim]);

  async function bootstrap(): Promise<void> {
    try {
      const [savedToken, savedProfileId] = await Promise.all([
        AsyncStorage.getItem(TOKEN_KEY),
        AsyncStorage.getItem(PROFILE_ID_KEY),
      ]);
      if (savedToken) {
        setToken(savedToken);
        setProfileId(savedProfileId ? Number(savedProfileId) : null);
        await loadDashboard(savedToken);
      }
    } catch (error) {
      Alert.alert("Session error", getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  async function loadDashboard(authToken: string): Promise<void> {
    setRefreshing(true);
    try {
      const [myProfile, myPosts, myFeed] = await Promise.all([
        apiGetMyProfile(authToken),
        apiGetMyPosts(authToken),
        apiGetMyFeed(authToken),
      ]);
      setProfile(myProfile);
      setPosts(myPosts);
      setFeed(myFeed);
      setProfileId(myProfile.id);
    } catch (error) {
      Alert.alert("API error", getErrorMessage(error));
    } finally {
      setRefreshing(false);
    }
  }

  async function handleLogin(): Promise<void> {
    if (!username || !password) {
      Alert.alert("Missing input", "Enter username and password.");
      return;
    }

    setLoading(true);
    try {
      const result: LoginResponse = await apiLogin(username.trim(), password);
      setToken(result.token);
      setProfileId(result.profile.id);
      await AsyncStorage.setItem(TOKEN_KEY, result.token);
      await AsyncStorage.setItem(PROFILE_ID_KEY, String(result.profile.id));
      await loadDashboard(result.token);
      setPassword("");
    } catch (error) {
      Alert.alert("Login failed", getErrorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  async function handleLogout(): Promise<void> {
    await AsyncStorage.multiRemove([TOKEN_KEY, PROFILE_ID_KEY]);
    setToken(null);
    setProfile(null);
    setPosts([]);
    setFeed([]);
    setCaption("");
    setImageUrl("");
    setUsername("");
    setPassword("");
    fadeAnim.setValue(0);
  }

  async function handleCreatePost(): Promise<void> {
    if (!caption.trim() && !imageUrl.trim()) {
      Alert.alert("Missing data", "Enter a caption or an image URL.");
      return;
    }

    if (!token) {
      Alert.alert("Auth error", "Please login again.");
      return;
    }

    setRefreshing(true);
    try {
      await apiCreatePost(token, {
        caption: caption.trim(),
        image_url: imageUrl.trim(),
      });
      setCaption("");
      setImageUrl("");
      await loadDashboard(token);
      Alert.alert("Success", "Post created.");
    } catch (error) {
      Alert.alert("Create post failed", getErrorMessage(error));
    } finally {
      setRefreshing(false);
    }
  }

  if (loading) {
    return (
      <SafeAreaView style={styles.loadingWrap}>
        <StatusBar barStyle="light-content" />
        <ActivityIndicator size="large" color="#ffd166" />
      </SafeAreaView>
    );
  }

  if (!token) {
    return (
      <LinearGradient colors={["#0b132b", "#1c2541", "#3a506b"]} style={styles.bg}>
        <SafeAreaView style={styles.safeArea}>
          <StatusBar barStyle="light-content" />
          <View style={styles.loginCard}>
            <Text style={styles.brand}>MiniInsta</Text>
            <Text style={styles.tagline}>Mobile client for your Django REST API</Text>
            <TextInput
              value={username}
              onChangeText={setUsername}
              placeholder="Username"
              placeholderTextColor="#90a4ae"
              style={styles.input}
              autoCapitalize="none"
            />
            <TextInput
              value={password}
              onChangeText={setPassword}
              placeholder="Password"
              placeholderTextColor="#90a4ae"
              style={styles.input}
              secureTextEntry
              autoCapitalize="none"
              autoCorrect={false}
            />
            <Pressable style={styles.primaryBtn} onPress={handleLogin}>
              <Text style={styles.primaryBtnText}>Sign In</Text>
            </Pressable>
          </View>
        </SafeAreaView>
      </LinearGradient>
    );
  }

  return (
    <LinearGradient colors={["#001219", "#005f73", "#0a9396"]} style={styles.bg}>
      <SafeAreaView style={styles.safeArea}>
        <StatusBar barStyle="light-content" />
        <Animated.View style={{ opacity: fadeAnim, flex: 1 }}>
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={styles.rowBetween}>
              <View>
                <Text style={styles.heading}>Welcome back</Text>
                <Text style={styles.subHeading}>Profile #{profileId}</Text>
              </View>
              <Pressable style={styles.ghostBtn} onPress={handleLogout}>
                <Text style={styles.ghostBtnText}>Logout</Text>
              </Pressable>
            </View>

            {profile && (
              <View style={styles.card}>
                <Text style={styles.cardTitle}>My Profile</Text>
                <Text style={styles.name}>{profile.display_name || profile.username}</Text>
                <Text style={styles.meta}>@{profile.username}</Text>
                <Text style={styles.meta}>{profile.bio_text || "No bio yet"}</Text>
                <Text style={styles.meta}>
                  Followers: {profile.num_followers} | Following: {profile.num_following}
                </Text>
              </View>
            )}

            <View style={styles.card}>
              <Text style={styles.cardTitle}>Create Post</Text>
              <TextInput
                value={caption}
                onChangeText={setCaption}
                placeholder="Write a caption"
                placeholderTextColor="#7f8c8d"
                style={styles.inputLight}
              />
              <TextInput
                value={imageUrl}
                onChangeText={setImageUrl}
                placeholder="Optional image URL"
                placeholderTextColor="#7f8c8d"
                style={styles.inputLight}
                autoCapitalize="none"
              />
              <Pressable style={styles.primaryBtn} onPress={handleCreatePost}>
                <Text style={styles.primaryBtnText}>Publish</Text>
              </Pressable>
            </View>

            <View style={styles.card}>
              <View style={styles.rowBetween}>
                <Text style={styles.cardTitle}>My Posts ({posts.length})</Text>
                <Pressable onPress={() => void loadDashboard(token)}>
                  <Text style={styles.link}>Refresh</Text>
                </Pressable>
              </View>
              {refreshing ? <ActivityIndicator color="#005f73" /> : null}
              {posts.map((post) => (
                <PostItem key={`mypost-${post.id}`} post={post} />
              ))}
              {!posts.length && <Text style={styles.empty}>No posts yet.</Text>}
            </View>

            <View style={styles.card}>
              <Text style={styles.cardTitle}>My Feed ({feed.length})</Text>
              {feed.map((post) => (
                <PostItem key={`feed-${post.id}`} post={post} />
              ))}
              {!feed.length && <Text style={styles.empty}>Your feed is empty.</Text>}
            </View>
          </ScrollView>
        </Animated.View>
      </SafeAreaView>
    </LinearGradient>
  );
}

type PostItemProps = {
  post: Post;
};

function PostItem({ post }: PostItemProps): React.JSX.Element {
  const firstPhoto = post.photos?.[0]?.image;

  return (
    <View style={styles.postItem}>
      <Text style={styles.postCaption}>{post.caption || "(no caption)"}</Text>
      <Text style={styles.postMeta}>Post #{post.id}</Text>
      {firstPhoto ? <Image source={{ uri: firstPhoto }} style={styles.photo} /> : null}
    </View>
  );
}

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unexpected error";
}

const styles = StyleSheet.create({
  bg: { flex: 1 },
  safeArea: { flex: 1, paddingHorizontal: 16, paddingTop: 12 },
  loadingWrap: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#001219",
  },
  loginCard: {
    backgroundColor: "rgba(255, 255, 255, 0.08)",
    borderRadius: 18,
    padding: 20,
    marginTop: 80,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.15)",
  },
  brand: {
    color: "#ffd166",
    fontSize: 36,
    fontWeight: "800",
    letterSpacing: 1,
    marginBottom: 8,
  },
  tagline: {
    color: "#e0fbfc",
    marginBottom: 18,
    fontSize: 14,
  },
  input: {
    backgroundColor: "#0b132b",
    color: "#ffffff",
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 10,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: "#3a506b",
  },
  inputLight: {
    backgroundColor: "#e9f5f5",
    color: "#001219",
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 10,
  },
  primaryBtn: {
    backgroundColor: "#ee9b00",
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: "center",
  },
  primaryBtnText: {
    color: "#001219",
    fontWeight: "700",
    fontSize: 16,
  },
  ghostBtn: {
    borderWidth: 1,
    borderColor: "#94d2bd",
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  ghostBtnText: {
    color: "#e9f5db",
    fontWeight: "600",
  },
  scrollContent: {
    paddingBottom: 36,
    gap: 14,
  },
  rowBetween: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  heading: {
    color: "#e9f5db",
    fontSize: 26,
    fontWeight: "700",
  },
  subHeading: {
    color: "#94d2bd",
    marginTop: 2,
  },
  card: {
    backgroundColor: "#f1faee",
    borderRadius: 16,
    padding: 14,
    shadowColor: "#000",
    shadowOpacity: 0.15,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
  },
  cardTitle: {
    color: "#005f73",
    fontSize: 18,
    fontWeight: "700",
    marginBottom: 8,
  },
  name: {
    fontSize: 20,
    fontWeight: "700",
    color: "#001219",
  },
  meta: {
    color: "#344e41",
    marginTop: 2,
  },
  link: {
    color: "#0a9396",
    fontWeight: "700",
  },
  postItem: {
    borderTopWidth: 1,
    borderTopColor: "#d9e6e6",
    paddingTop: 10,
    marginTop: 8,
  },
  postCaption: {
    color: "#001219",
    fontSize: 16,
    fontWeight: "600",
  },
  postMeta: {
    color: "#587271",
    marginTop: 2,
    marginBottom: 8,
  },
  photo: {
    width: "100%",
    height: 170,
    borderRadius: 10,
    backgroundColor: "#d8f3dc",
  },
  empty: {
    color: "#6c757d",
    marginTop: 6,
  },
});
