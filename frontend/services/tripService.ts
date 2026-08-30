import type { Trip, TripInput } from "@/types/trip";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

// Helper to get authorization header
function getAuthHeader(): HeadersInit {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  return headers;
}

async function parseResponse<T>(response: Response): Promise<T> {
  if (response.status === 401) {
    // Token expired or invalid - clear storage and redirect to login
    if (typeof window !== "undefined") {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    throw new Error("Your session has expired. Please login again.");
  }
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Unable to load your trips. Please try again.");
  }
  
  return response.json() as Promise<T>;
}

export async function getTrips(): Promise<Trip[]> {
  return parseResponse<Trip[]>(
    await fetch(`${API_URL}/trips`, {
      method: "GET",
      headers: getAuthHeader(),
      cache: "no-store",
    })
  );
}

export async function getTrip(id: number): Promise<Trip> {
  return parseResponse<Trip>(
    await fetch(`${API_URL}/trips/${id}`, {
      method: "GET",
      headers: getAuthHeader(),
      cache: "no-store",
    })
  );
}

export async function generateTrip(data: TripInput): Promise<Trip> {
  return parseResponse<Trip>(
    await fetch(`${API_URL}/trips`, {
      method: "POST",
      headers: getAuthHeader(),
      body: JSON.stringify(data),
    })
  );
}

export async function updateTrip(id: number, data: { budget: number }): Promise<Trip> {
  return parseResponse<Trip>(
    await fetch(`${API_URL}/trips/${id}`, {
      method: "PUT",
      headers: getAuthHeader(),
      body: JSON.stringify(data),
    })
  );
}

export async function deleteTrip(id: number): Promise<{ message: string }> {
  return parseResponse<{ message: string }>(
    await fetch(`${API_URL}/trips/${id}`, {
      method: "DELETE",
      headers: getAuthHeader(),
    })
  );
}
