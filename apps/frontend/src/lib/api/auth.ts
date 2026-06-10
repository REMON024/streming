import api from './client';

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  user: {
    id: string;
    email: string;
    name: string;
    subscriptionTier: number;
  };
  accessToken: string;
  refreshToken: string;
}

export async function login(payload: LoginPayload): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>('/api/auth/login', payload);
  return data;
}

export async function register(payload: RegisterPayload): Promise<{ message: string }> {
  const { data } = await api.post('/api/auth/register', payload);
  return data;
}

export async function logout(): Promise<void> {
  try {
    await api.post('/api/auth/logout');
  } catch {
    // Ignore logout errors
  }
}

export async function refreshToken(token: string): Promise<AuthResponse> {
  const { data } = await api.post<AuthResponse>('/api/auth/refresh', { refreshToken: token });
  return data;
}

export async function getMe(): Promise<AuthResponse['user']> {
  const { data } = await api.get('/api/users/me');
  return data;
}
