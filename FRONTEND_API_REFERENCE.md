# SpyNet Backend API Reference

**Base URL:** `https://unshouting-mindi-nonrevocably.ngrok-free.dev`

All authenticated requests require JWT token in the header:
```
Authorization: Bearer <your-access-token>
```

## Authentication Endpoints

### 1. Sign Up
**POST** `/auth/signup`

Create a new user account.

**Request Body:**
```typescript
{
  name: string;      // User's full name
  email: string;     // User's email
  password: string;   // User's password
  role: "detective" | "manager";  // User role
}
```

**Response:**
```typescript
{
  user: {
    id: string;
    name: string;
    email: string;
    role: "detective" | "manager";
    created_at: string;
  };
  access_token: string | null;  // JWT token (null if email confirmation required)
}
```

**Example:**
```typescript
const response = await fetch(`${API_BASE_URL}/auth/signup`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "John Detective",
    email: "john@example.com",
    password: "SecurePass123!",
    role: "detective"
  })
});
```

---

### 2. Login
**POST** `/auth/login`

Login an existing user.

**Request Body:**
```typescript
{
  email: string;
  password: string;
}
```

**Response:**
```typescript
{
  user: {
    id: string;
    name: string;
    email: string;
    role: "detective" | "manager";
    created_at: string;
  };
  access_token: string;  // JWT token
}
```

---

## User Endpoints

### 3. List All Users (Manager Only)
**GET** `/users`

Get all users in the system. **Requires manager role.**

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```typescript
Array<{
  id: string;
  name: string;
  email: string;
  role: "detective" | "manager";
  created_at: string;
}>
```

---

### 4. List Detectives
**GET** `/users/detectives?manager_id=<manager_id>`

Get all users with role="detective". Optionally filter by assigned manager.

**Query Parameters:**
- `manager_id` (optional): Filter detectives by assigned manager ID

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```typescript
Array<{
  id: string;
  name: string;
  email: string;
  role: "detective";
  manager_id: string | null;  // Assigned manager ID
  created_at: string;
}>
```

**Example:**
```typescript
// Get all detectives
GET /users/detectives

// Get detectives assigned to a specific manager
GET /users/detectives?manager_id=abc-123
```

---

### 4b. Get My Detectives (Manager Only)
**GET** `/users/my-detectives`

Get detectives assigned to the logged-in manager.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** Same as List Detectives above

**Note:** Only returns detectives assigned to the authenticated manager

---

### 5. Get User by ID
**GET** `/users/{user_id}`

Get specific user details. Detective can only view their own profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  id: string;
  name: string;
  email: string;
  role: "detective" | "manager";
  created_at: string;
}
```

---

### 6. Update User
**PUT** `/users/{user_id}`

Update user information. Managers can update any field. Users can only update their own name.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```typescript
{
  name?: string;
  email?: string;     // Managers only
  role?: "detective" | "manager";  // Managers only
}
```

**Response:** Updated user object

---

## Case Endpoints

### 7. List Cases
**GET** `/cases?status=<status>&detective_id=<id>`

List all cases. Managers see all cases, detectives see only their own.

**Query Parameters:**
- `status` (optional): Filter by "open" | "in_progress" | "closed"
- `detective_id` (optional): Filter by detective ID

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```typescript
Array<{
  id: string;
  title: string;
  details: string;
  location: string;
  status: "open" | "in_progress" | "closed";
  detective_id: string | null;
  created_at: string;
  updated_at: string;
}>
```

**Example:**
```typescript
// Get all cases
GET /cases

// Get cases with status filter
GET /cases?status=open

// Get cases for specific detective
GET /cases?detective_id=abc-123
```

---

### 8. Get Case by ID
**GET** `/cases/{case_id}`

Get specific case details. Detective can only view their own cases.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  id: string;
  title: string;
  details: string;
  location: string;
  status: "open" | "in_progress" | "closed";
  detective_id: string | null;
  created_at: string;
  updated_at: string;
}
```

---

### 9. Create Case (Manager Only)
**POST** `/cases`

Create a new case. **Requires manager role.**

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```typescript
{
  title: string;
  details: string;
  location: string;
  status?: "open" | "in_progress" | "closed";  // Default: "open"
  detective_id?: string;  // Optional: assign to detective
}
```

**Response:** Created case object

**Example:**
```typescript
{
  title: "Missing Person",
  details: "Person reported missing near downtown",
  location: "123 Main St",
  status: "open",  // Optional
  detective_id: "abc-123"  // Optional
}
```

---

### 10. Update Case
**PUT** `/cases/{case_id}`

Update case information. Managers can update all fields. Detectives can only update status and details of their own cases.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```typescript
{
  title?: string;     // Managers only
  details?: string;   // Managers can update all; Detectives can update
  location?: string;  // Managers only
  status?: "open" | "in_progress" | "closed";  // All can update
  detective_id?: string;  // Managers only
}
```

**Response:** Updated case object

---

### 11. Delete Case (Manager Only)
**DELETE** `/cases/{case_id}`

Delete a case permanently. **Requires manager role.**

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** 204 No Content (empty body)

---

## Complete TypeScript API Helper

```typescript
const API_BASE_URL = "https://unshouting-mindi-nonrevocably.ngrok-free.dev";

// Helper to get auth header
const getAuthHeader = (token: string) => ({
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json",
  "ngrok-skip-browser-warning": "true"
});

// Helper function
async function apiCall<T>(endpoint: string, options?: RequestInit, token?: string): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true",
    ...(token && { "Authorization": `Bearer ${token}` }),
    ...options?.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API error (${response.status}): ${errorText}`);
  }

  if (response.status === 204) return {} as T; // No Content
  return response.json();
}

// ===== AUTH =====
export const authAPI = {
  signup: async (name: string, email: string, password: string, role: "detective" | "manager" = "detective") => {
    return apiCall<{ user: any; access_token: string | null }>("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ name, email, password, role }),
    });
  },

  login: async (email: string, password: string) => {
    return apiCall<{ user: any; access_token: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  },
};

// ===== USERS =====
export const usersAPI = {
  getAll: async (token: string) => {
    return apiCall<any[]>("/users", { method: "GET" }, token);
  },

  getDetectives: async (token: string, managerId?: string) => {
    const endpoint = managerId ? `/users/detectives?manager_id=${managerId}` : "/users/detectives";
    return apiCall<any[]>(endpoint, { method: "GET" }, token);
  },

  getMyDetectives: async (token: string) => {
    return apiCall<any[]>("/users/my-detectives", { method: "GET" }, token);
  },

  getById: async (userId: string, token: string) => {
    return apiCall<any>(`/users/${userId}`, { method: "GET" }, token);
  },

  update: async (userId: string, data: { name?: string; email?: string; role?: string }, token: string) => {
    return apiCall<any>(`/users/${userId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }, token);
  },
};

// ===== CASES =====
export const casesAPI = {
  getAll: async (token: string, filters?: { status?: string; detective_id?: string }) => {
    const params = new URLSearchParams();
    if (filters?.status) params.append("status", filters.status);
    if (filters?.detective_id) params.append("detective_id", filters.detective_id);
    const query = params.toString();
    return apiCall<any[]>(`/cases${query ? `?${query}` : ""}`, { method: "GET" }, token);
  },

  getById: async (caseId: string, token: string) => {
    return apiCall<any>(`/cases/${caseId}`, { method: "GET" }, token);
  },

  create: async (data: { title: string; details: string; location: string; status?: string; detective_id?: string }, token: string) => {
    return apiCall<any>("/cases", {
      method: "POST",
      body: JSON.stringify(data),
    }, token);
  },

  update: async (caseId: string, data: { title?: string; details?: string; location?: string; status?: string; detective_id?: string }, token: string) => {
    return apiCall<any>(`/cases/${caseId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }, token);
  },

  delete: async (caseId: string, token: string) => {
    return apiCall(`/cases/${caseId}`, { method: "DELETE" }, token);
  },
};
```

---

## Usage Examples

### Signup and Login
```typescript
// Signup
const { user, access_token } = await authAPI.signup(
  "John Doe",
  "john@example.com", 
  "password123",
  "detective"
);
localStorage.setItem("token", access_token);
localStorage.setItem("user", JSON.stringify(user));

// Login
const { user, access_token } = await authAPI.login(
  "john@example.com",
  "password123"
);
```

### Get Cases (with Authentication)
```typescript
const token = localStorage.getItem("token");
const cases = await casesAPI.getAll(token, { status: "open" });
```

### Create Case (Manager Only)
```typescript
const token = localStorage.getItem("token");
const newCase = await casesAPI.create({
  title: "Case Title",
  details: "Case description",
  location: "Location",
  detective_id: "detective-uuid"
}, token);
```

### Update Case Status (Detective)
```typescript
const token = localStorage.getItem("token");
await casesAPI.update(caseId, { status: "in_progress" }, token);
```

### Assign Detective to Manager
```typescript
const token = localStorage.getItem("token");
await usersAPI.update(detectiveId, { manager_id: managerId }, token);
```

### Get Detectives for a Manager
```typescript
const token = localStorage.getItem("token");

// Get all my detectives (authenticated manager)
const myDetectives = await usersAPI.getMyDetectives(token);

// Get all detectives assigned to a specific manager
const assignedDetectives = await usersAPI.getDetectives(token, managerId);
```

---

## Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `400` - Bad Request
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

