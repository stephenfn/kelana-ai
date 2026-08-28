import type { Trip, TripInput } from "@/types/trip";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) throw new Error("Unable to load your trips. Please try again.");
  return response.json() as Promise<T>;
}

export async function getTrips(): Promise<Trip[]> {
  return parseResponse<Trip[]>(await fetch(`${API_URL}/trips`, { cache: "no-store" }));
}

export async function getTrip(id: number): Promise<Trip> {
  return parseResponse<Trip>(await fetch(`${API_URL}/trips/${id}`, { cache: "no-store" }));
}

export async function generateTrip(data: TripInput): Promise<Trip> {
  return parseResponse<Trip>(await fetch(`${API_URL}/trips`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }));
}
