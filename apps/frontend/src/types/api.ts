export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
  hasNextPage: boolean;
  hasPreviousPage: boolean;
}

export interface ApiError {
  message: string;
  statusCode: number;
  errors?: Record<string, string[]>;
  timestamp?: string;
  path?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}
