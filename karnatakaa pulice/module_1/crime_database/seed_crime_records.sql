INSERT INTO crime_records (
    crime_id, police_station, district, crime_type, crime_date, crime_time,
    victim, suspect, vehicle, weapon, latitude, longitude, status, notes
) VALUES
(
    'KA-BLR-2026-0001', 'Indiranagar Police Station', 'Bengaluru Urban',
    'Vehicle Theft', '2026-06-14', '22:15:00', 'Ravi Kumar', 'Unknown',
    'KA-03-MN-4182', NULL, 12.978400, 77.640800, 'Open',
    'Two-wheeler reported stolen near metro parking.'
),
(
    'KA-MYS-2026-0002', 'Lashkar Police Station', 'Mysuru',
    'Robbery', '2026-06-18', '20:40:00', 'Anita Rao', 'Mahesh S',
    NULL, 'Knife', 12.308600, 76.653100, 'Under Investigation',
    'Suspect identified through nearby CCTV footage.'
),
(
    'KA-HBL-2026-0003', 'Hubballi Town Police Station', 'Dharwad',
    'Burglary', '2026-06-21', '02:30:00', 'Commercial Store', 'Unknown',
    'White van', 'Crowbar', 15.364700, 75.124000, 'Open',
    'Pattern matches two recent night burglaries.'
);
