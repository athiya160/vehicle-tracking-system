import 'package:flutter_test/flutter_test.dart';
import 'package:vehicle_tracking_app/features/auth/domain/user_entity.dart';
import 'package:vehicle_tracking_app/features/tracking/domain/tracking_entities.dart';
import 'package:latlong2/latlong.dart';

void main() {
  test('UserEntity equality and properties test', () {
    const user1 = UserEntity(
      id: 1,
      username: 'usera',
      email: 'usera@example.com',
      routeId: 1,
      vehicleId: 1,
    );

    const user2 = UserEntity(
      id: 1,
      username: 'usera',
      email: 'usera@example.com',
      routeId: 1,
      vehicleId: 1,
    );

    expect(user1, equals(user2));
    expect(user1.username, 'usera');
  });

  test('GPSLocationEntity calculation and position test', () {
    final location = GPSLocationEntity(
      vehicleId: 1,
      vehicleNumber: 'BUS-001',
      latitude: 12.9716,
      longitude: 77.5946,
      speed: 42.5,
      timestamp: DateTime.now(),
    );

    expect(location.position, const LatLng(12.9716, 77.5946));
    expect(location.speed, 42.5);
    expect(location.vehicleNumber, 'BUS-001');
  });

  test('RouteEntity coordinates verification', () {
    const route = RouteEntity(
      id: 1,
      name: 'Route A',
      startLocation: 'Bangalore',
      endLocation: 'Hassan',
      coordinates: [
        LatLng(12.9716, 77.5946),
        LatLng(13.0068, 76.1004),
      ],
    );

    expect(route.coordinates.length, 2);
    expect(route.name, 'Route A');
  });
}
