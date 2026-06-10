package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/golang-jwt/jwt/v5"
	"streaming/internal/config"
)

type contextKey string

const (
	UserIDKey           contextKey = "userId"
	SubscriptionTierKey contextKey = "subscriptionTier"
)

// RequireJWT validates a Bearer token from the Authorization header.
func RequireJWT(cfg *config.Config) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			tokenStr := extractToken(r)
			if tokenStr == "" {
				http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
				return
			}
			claims, err := validateJWT(tokenStr, cfg.JWTSecret)
			if err != nil {
				http.Error(w, `{"error":"invalid token"}`, http.StatusUnauthorized)
				return
			}
			ctx := context.WithValue(r.Context(), UserIDKey, claims["sub"])
			tier, _ := claims["tier"].(float64)
			ctx = context.WithValue(ctx, SubscriptionTierKey, int(tier))
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

// RequireJWTFromQuery validates a Bearer token from the Authorization header
// or, as a fallback, from the ?token= query parameter (used for .ts segment requests
// where the player cannot set custom headers).
func RequireJWTFromQuery(cfg *config.Config) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			tokenStr := extractToken(r)
			if tokenStr == "" {
				tokenStr = r.URL.Query().Get("token")
			}
			if tokenStr == "" {
				http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
				return
			}
			claims, err := validateJWT(tokenStr, cfg.JWTSecret)
			if err != nil {
				http.Error(w, `{"error":"invalid token"}`, http.StatusUnauthorized)
				return
			}
			ctx := context.WithValue(r.Context(), UserIDKey, claims["sub"])
			tier, _ := claims["tier"].(float64)
			ctx = context.WithValue(ctx, SubscriptionTierKey, int(tier))
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

// RequireInternalKey validates the X-Internal-Key header for service-to-service calls.
func RequireInternalKey(cfg *config.Config) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			key := r.Header.Get("X-Internal-Key")
			if key != cfg.InternalAPIKey {
				http.Error(w, `{"error":"forbidden"}`, http.StatusForbidden)
				return
			}
			next.ServeHTTP(w, r)
		})
	}
}

func extractToken(r *http.Request) string {
	auth := r.Header.Get("Authorization")
	if strings.HasPrefix(auth, "Bearer ") {
		return strings.TrimPrefix(auth, "Bearer ")
	}
	return ""
}

func validateJWT(tokenStr, secret string) (jwt.MapClaims, error) {
	token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return []byte(secret), nil
	})
	if err != nil || !token.Valid {
		return nil, err
	}
	return token.Claims.(jwt.MapClaims), nil
}
