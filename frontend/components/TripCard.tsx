import Link from "next/link";
import type { Trip } from "@/types/trip";

const flags: Record<string, string> = { japan: "🇯🇵", bali: "🌴", singapore: "🇸🇬", france: "🇫🇷", italy: "🇮🇹" };

function badgeClass(value: string) {
  const normalized = value.toLowerCase();
  if (normalized.includes("backpacker")) return "badge badge-orange";
  if (normalized.includes("luxury")) return "badge badge-purple";
  return "badge badge-green";
}

export function TripCard({ trip }: { trip: Trip }) {
  const flag = flags[trip.destination.toLowerCase()] ?? "✈️";
  return (
    <Link href={`/trips/${trip.id}`} className="trip-card group">
      <div className="trip-icon" aria-hidden="true">{flag}</div>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-2"><h2 className="truncate text-xl font-bold text-[#163849]">{trip.destination}</h2><span className={badgeClass(trip.category)}>{trip.category}</span></div>
        <p className="mt-2 text-sm text-[#587077]">{trip.days} days <span className="mx-1 text-[#b4c5c4]">·</span> USD {trip.budget.toLocaleString()} <span className="mx-1 text-[#b4c5c4]">·</span> {trip.category}</p>
        <span className="mt-4 inline-block text-sm font-bold text-[#168b82] transition group-hover:translate-x-1">View details <span aria-hidden="true">→</span></span>
      </div>
    </Link>
  );
}
