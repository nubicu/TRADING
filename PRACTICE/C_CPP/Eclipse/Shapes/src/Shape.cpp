#include "Shape.hpp"

Shape::Shape(Coord2D coord) {
	moveTo(coord);
}

Shape::Shape(const Shape& other) {
	coordinates = other.coordinates;
}

Shape::~Shape() {}

void Shape::moveTo(Coord2D coord) {
	coordinates.x = coord.x;
	coordinates.y = coord.y;
}

void Shape::moveBy(Coord2D relCoord) {
	coordinates.x += relCoord.x;
	coordinates.y += relCoord.y;
	moveTo(coordinates);
}

void Shape::resize(double factor) {
	coordinates.x *= factor;
	coordinates.y *= factor;
}

void Shape::draw() const {}

bool Shape::containsCoordinates(Coord2D coord) const{
	if ((coordinates.x == coord.x) && (coordinates.y == coord.y)) {
		return true;
	}
	return false;
}

