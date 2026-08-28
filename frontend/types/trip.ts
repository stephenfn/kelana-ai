export type Trip = {
  id: number;
  destination: string;
  budget: number;
  days: number;
  category: string;
  daily_budget: number;
};

export type TripInput = {
  destination: string;
  budget: number;
  days: number;
  travel_style?: string;
};
