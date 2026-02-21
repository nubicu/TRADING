#ifndef CIRCLE_HPP_
#define CIRCLE_HPP_

#include "Helper.hpp"
#include "Shape.hpp"

class Circle : public Shape {
public :
	Circle(Coord2D center, double radius);
	void resize(double factor);
	void draw() const;
	bool containsCoordinates(Coord2D coord) const;
private :
	double radius;
};




#endif /* CIRCLE_HPP_ */
