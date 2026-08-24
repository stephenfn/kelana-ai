"use client";

import { FormEvent, useMemo, useState } from "react";

type TripForm = {
  destination: string;
  budget: string;
  days: string;
  travel_style: string;
};

type SavedTrip = {
  id: number;
  destination: string;
  budget: number;
  days: number;
  category: string;
  daily_budget: number;
};

const defaultForm: TripForm = {
  destination: "Japan",
  budget: "2000",
  days: "5",
  travel_style: "Family",
};

function buildRecommendation(destination: string, days: number) {
  const places = [
    `Day 1: Explore ${destination} with a gentle city walk, local food stops, and a culturally rich landmark.`,
    `Day 2: Visit the best neighborhoods and hidden gems, with time for shopping and a relaxed coffee break.`,
    `Day 3: Enjoy a local experience like a market visit, scenic viewpoint, or iconic attraction.`,
    `Day 4: Take a day trip or a slow cultural experience to better understand the local rhythm.`,
    `Day 5: Finish with a memorable evening and a relaxed dinner in a lively area.`,
  ];

  return places.slice(0, Math.max(1, Math.min(days, places.length)));
}

export default function Home() {
  const [form, setForm] = useState<TripForm>(defaultForm);
  const [trip, setTrip] = useState<SavedTrip | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const itinerary = useMemo(() => {
    if (!trip) return [];
    return buildRecommendation(trip.destination, trip.days);
  }, [trip]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/api/v1/trips", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          destination: form.destination,
          budget: Number(form.budget),
          days: Number(form.days),
          travel_style: form.travel_style,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to generate itinerary. Please try again.");
      }

      const data: SavedTrip = await response.json();
      setTrip(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to generate itinerary. Please try again.",
      );
      setTrip(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-100 px-4 py-8 text-slate-900 md:px-8">
      <div className="mx-auto max-w-6xl">
        <header className="mb-6 flex items-center gap-3">
          <div className="h-8 w-8 rounded-md bg-gradient-to-br from-sky-500 to-blue-700 shadow-sm" />
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.22em] text-sky-700">
              KELANAAI · SESSION 6
            </p>
            <h1 className="text-3xl font-black md:text-5xl">KelanaAI</h1>
          </div>
        </header>

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-sky-500 bg-white p-5 shadow-sm md:p-7">
            <h2 className="mb-6 text-2xl font-bold text-sky-700">Plan your next adventure</h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <label className="block">
                <span className="mb-2 block text-sm font-semibold uppercase tracking-wide text-slate-600">
                  Destination
                </span>
                <input
                  value={form.destination}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, destination: event.target.value }))
                  }
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-lg outline-none transition focus:border-sky-500 focus:bg-white"
                  placeholder="Japan"
                />
              </label>

              <label className="block">
                <span className="mb-2 block text-sm font-semibold uppercase tracking-wide text-slate-600">
                  Budget (USD)
                </span>
                <input
                  type="number"
                  min="1"
                  value={form.budget}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, budget: event.target.value }))
                  }
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-lg outline-none transition focus:border-sky-500 focus:bg-white"
                />
              </label>

              <label className="block">
                <span className="mb-2 block text-sm font-semibold uppercase tracking-wide text-slate-600">
                  Days
                </span>
                <input
                  type="number"
                  min="1"
                  max="30"
                  value={form.days}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, days: event.target.value }))
                  }
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-lg outline-none transition focus:border-sky-500 focus:bg-white"
                />
              </label>

              <label className="block">
                <span className="mb-2 block text-sm font-semibold uppercase tracking-wide text-slate-600">
                  Travel style
                </span>
                <input
                  value={form.travel_style}
                  onChange={(event) =>
                    setForm((current) => ({ ...current, travel_style: event.target.value }))
                  }
                  className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-lg outline-none transition focus:border-sky-500 focus:bg-white"
                  placeholder="Family"
                />
              </label>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-xl bg-sky-600 px-4 py-3 text-lg font-semibold text-white shadow-md transition hover:bg-sky-700 disabled:cursor-not-allowed disabled:bg-sky-400"
              >
                {loading ? "Generating itinerary..." : "Generate AI Trip"}
              </button>
            </form>
          </div>

          <div className="rounded-2xl border border-sky-500 bg-white p-5 shadow-sm md:p-7">
            <div className="mb-4 flex items-center justify-between gap-3">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                  Destination
                </p>
                <h3 className="text-xl font-bold text-slate-800">
                  {trip ? trip.destination : form.destination || "Your trip"}
                </h3>
              </div>
              <div className="rounded-xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700">
                Budget: ${trip ? trip.budget : Number(form.budget || 0).toLocaleString()}
              </div>
            </div>

            {loading && (
              <div className="mt-4 rounded-2xl bg-gradient-to-r from-teal-500 to-sky-600 p-6 text-center text-white shadow-inner">
                <div className="mx-auto mb-3 h-10 w-10 rounded-full border-4 border-white/40 border-t-white animate-spin" />
                <p className="text-xl font-semibold">Generating itinerary...</p>
                <p className="mt-2 text-sm text-teal-50">KelanaAI is thinking.</p>
              </div>
            )}

            {error && (
              <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-red-700">
                {error}
              </div>
            )}

            {!loading && !error && itinerary.length > 0 && (
              <div className="mt-4 space-y-3">
                <h4 className="text-xs font-semibold uppercase tracking-[0.2em] text-sky-700">
                  AI Recommendation
                </h4>
                {itinerary.map((item) => (
                  <div
                    key={item}
                    className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-700"
                  >
                    {item}
                  </div>
                ))}
              </div>
            )}

            {!loading && !error && itinerary.length === 0 && (
              <div className="mt-4 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-6 text-slate-500">
                Ready to generate your next itinerary.
              </div>
            )}
          </div>
        </section>
      </div>
    </main>
  );
}
