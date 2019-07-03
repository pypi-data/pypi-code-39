import math
from gaia_router.macros import GPS_PRECISION

# rota sera subida e decida, tipo comprimento de onda
# funcsobeedesce()->verifica se sobe x->se puder, x++, senao fim de rota
# ->iterar pelo y ascendentemente sempre adicionando o par de coordenadas na
# rota
# ->verifica se pode subir x->se puder, x++,senao fim de rota
# ->iterar pelo y descendentemente sempre adicionando o par de coordenadas na
#  rota->repete

# enquanto estiver em coleta, vou chamar sobeedesce ate acabar
# border_points_array rota.
# funcao de desvio deve funcionar do msm jeito


class MapRouter():
    """
    Class with the mapping functions for the router.
    """

    def __init__(self, begin, end, current, base):
        self.points = [begin, end]
        self.current_position = current
        self.base_location = base

    def _calculate_real_distance(point1, point2):
        distance_x = point2[0] - point1[0]
        distance_y = point2[1] - point1[1]

        real_distance = math.sqrt(
            (distance_x * distance_x) + (distance_y * distance_y))
        return real_distance, distance_x, distance_y

    def trace_route_to_base(self):
        """
        Traces border_points_array route back to the base.
        """
        return [self.base_location]

    def trace_collection_route(self):
        """
        Traces border_points_array route using the area of operations map.
        To trace the routes it is assumed that the points are in minutes if
        they are not in minutes conversion must happen before this method is
        used.
        """
        x = [self.points[0][0], self.points[1][0]]

        y = self.points[0][1]
        route = []
        i = 0
        while(y < self.points[1][1]):
            route.append((x[i], y))
            i = (i + 1) % 2
            route.append((x[i], y))
            y += GPS_PRECISION
        return route

    def set_current_pos(self, geolocation):
        """
        Setter for the current_pos attr.
        """
        self.current_position = geolocation

    def _get_center(self):
        """
        Gets the middle point inside the operation area.
        """
        return tuple(((self.points[1][0] - self.points[0][0]) / 2,
                      (self.points[1][1] - self.points[0][1]) / 2))

    def trace_evasion_route(self, route, angle):
        """
        Traces an evasion route given the next point must be evaded.
        """
        center = self._get_center()

        alpha = 60 * math.pi / 180
        beta = 300 * math.pi / 180

        alpha += angle
        beta += angle

        dis = GPS_PRECISION

        possible_points = []
        x = self.current_position[0]
        y = self.current_position[1]

        possible_points.append(
            tuple(
                (
                    (x + dis * math.cos(alpha)),
                    (y + dis * math.sin(alpha))
                )
            )
        )

        possible_points.append(
            tuple(
                (
                    (x + dis * math.cos(beta)),
                    (y + dis * math.sin(beta))
                )
            )
        )

        x0 = abs(center[0] - possible_points[0][0])
        y0 = abs(center[1] - possible_points[0][1])
        d0 = math.sqrt((x0*x0) + (y0*y0))

        x1 = abs(center[0] - possible_points[1][0])
        y1 = abs(center[1] - possible_points[1][1])
        d1 = math.sqrt((x1*x1) + (y1*y1))

        if(d0 < d1):
            return [possible_points[0]]

        else:
            return [possible_points[1]]

    def _get_borders(self):
        """
        Returns an array with the AO's borders.
        """
        border_points_array = []

        for i in range(abs(points[0][0] - points[1][0])):
            border_points_array.append(
                tuple(points[0][0] + (i * GPS_PRECISION), points[0][1]))

        for j in range(abs(points[0][1] - points[1][1])):
            border_points_array.append(
                tuple(points[0][0], points[0][1]) + (i * GPS_PRECISION))

        for i in range(abs(points[0][0] - points[1][0])):
            border_points_array.append(
                tuple(points[1][0] + (i * GPS_PRECISION), points[1][1]))

        for j in range(abs(points[0][1] - points[1][1])):
            border_points_array.append(
                tuple(points[1][0], points[1][1]) + (i * GPS_PRECISION))

        return border_points_array
