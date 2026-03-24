import csv
import math

TRUCK_CAPACITY = 100
MAX_TRUCKS = 4
CAPACITY_THRESHOLD = 0.85

def load_data(filepath):
    outlets = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            outlets.append({
                'id': row['outlet_id'],
                'zone': row['zone'],
                'stock': float(row['current_inventory_stock']),
                'offtake': float(row['average_weekly_offtake']),
                'order': float(row['order_quantity_cases']),
                'lat': float(row['lat']),
                'lon': float(row['lon'])
            })
    return outlets

def get_distance(p1, p2):
    return math.hypot(p1['lat'] - p2['lat'], p1['lon'] - p2['lon'])

def step1_demand_signals(outlets):
    print("\n--- STEP 1: Demand Signals ---")
    prioritized = []
    for o in outlets:
        woc = o['stock'] / o['offtake'] if o['offtake'] > 0 else 999
        if woc < 2.5:
            tier, priority = 'URGENT', 1
        elif woc <= 4.0:
            tier, priority = 'WATCH', 2
        else:
            tier, priority = 'OK', 3
            continue # Skip OK tier for delivery today
        
        o['woc'] = woc
        o['tier'] = tier
        o['priority'] = priority
        prioritized.append(o)
        print(f"{o['id']}: {woc:.1f} weeks ({tier})")
    
    return prioritized

def step2_clustering(outlets):
    zones = {}
    for o in outlets:
        zones.setdefault(o['zone'], []).append(o)
    return zones

def step3_greedy_load(zones):
    print("\n--- STEP 3: Greedy Load Building ---")
    trucks = []
    for zone, zone_outlets in zones.items():
        # Sort by urgency, then order quantity descending
        zone_outlets.sort(key=lambda x: (x['priority'], -x['order']))
        
        manifest = []
        loaded_vol = 0
        target_cap = TRUCK_CAPACITY * CAPACITY_THRESHOLD
        
        for o in zone_outlets:
            if loaded_vol + o['order'] <= target_cap:
                manifest.append(o)
                loaded_vol += o['order']
                
        truck={
            'zone': zone,
            'manifest': manifest,
            'total_vol': loaded_vol
        }
        trucks.append(truck)
        print(f"Truck allocated to {zone} -> {len(manifest)} stops, {loaded_vol} cases loaded.")
    return trucks

def step4_nearest_neighbour(trucks):
    print("\n--- STEP 4: Nearest-Neighbour Routing ---")
    wh_node = {'lat': 40.7128, 'lon': -74.0060} # Warehouse pseudo-coordinates
    
    for truck in trucks:
        unvisited = truck['manifest'].copy()
        current_node = wh_node
        route = []
        
        while unvisited:
            next_stop = min(unvisited, key=lambda x: get_distance(current_node, x))
            route.append(next_stop)
            unvisited.remove(next_stop)
            current_node = next_stop
            
        truck['route'] = route

    return trucks

def step5_dispatch_plan(trucks):
    print("\n--- STEP 5: Final Dispatch Plan ---")
    for i, truck in enumerate(trucks, 1):
        stops = len(truck['route'])
        cases = truck['total_vol']
        # Simulated route hours (just descriptive)
        hours = 8.0 + (stops * 0.5) + (cases * 0.01)
        print(f"Truck {i} · {truck['zone']:<7} · {stops} stops · {cases} cases · ~{hours:.1f}h")
        for stop in truck['route']:
            print(f"   -> Drop: {stop['id']} ({stop['tier']}, {stop['order']} cases)")

if __name__ == "__main__":
    data = load_data('delivery_demand.csv')
    filtered = step1_demand_signals(data)
    clustered = step2_clustering(filtered)
    trucks = step3_greedy_load(clustered)
    optimized_trucks = step4_nearest_neighbour(trucks)
    step5_dispatch_plan(optimized_trucks)
