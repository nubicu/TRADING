#include <iostream>
#include "Circle.hpp"

Circle::Circle(Coord2D center, double radius) : Shape(center), radius(radius) {

}

void Circle::resize(double factor) {
	this->resize(factor);
	std::cout << __PRETTY_FUNCTION__ << " " << this << std::endl;
}

void Circle::draw() const {
	std::cout << __PRETTY_FUNCTION__ << " " << this << std::endl;
}

bool Circle::containsCoordinates(Coord2D coord) const{
	return containsCoordinates(coord);
}


