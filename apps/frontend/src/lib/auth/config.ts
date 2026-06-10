import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import axios from 'axios';

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;

        try {
          const backendUrl = process.env.BACKEND_URL || 'http://localhost:5000';
          const { data } = await axios.post(`${backendUrl}/api/auth/login`, {
            email: credentials.email,
            password: credentials.password,
          });

          if (data.accessToken && data.user) {
            return {
              id: data.user.id,
              email: data.user.email,
              name: data.user.name,
              accessToken: data.accessToken,
              refreshToken: data.refreshToken,
              subscriptionTier: data.user.subscriptionTier ?? 0,
            };
          }
          return null;
        } catch (error) {
          return null;
        }
      },
    }),
  ],

  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = (user as any).accessToken;
        token.refreshToken = (user as any).refreshToken;
        token.subscriptionTier = (user as any).subscriptionTier;
        token.userId = (user as any).id;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        (session as any).accessToken = token.accessToken;
        (session as any).refreshToken = token.refreshToken;
        (session as any).subscriptionTier = token.subscriptionTier;
        session.user.id = token.userId as string;
      }
      return session;
    },
  },

  pages: {
    signIn: '/login',
    error: '/login',
  },

  secret: process.env.NEXTAUTH_SECRET,
  trustHost: true,
});
