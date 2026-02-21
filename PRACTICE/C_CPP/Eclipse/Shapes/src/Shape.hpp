#ifndef SHAPE_HPP_
#define SHAPE_HPP_

#include "Helper.hpp"

class Shape {
public :
	Shape(Coord2D coord);
	Shape(const Shape& other);
	virtual ~Shape();
	void moveTo(Coord2D coord);
	void moveBy(Coord2D relCoord);
	virtual void resize(double factor);
	virtual void draw() const;
	virtual bool containsCoordinates(Coord2D coord) const;
protected :
	Coord2D coordinates;
};



#endif /* SHAPE_HPP_ */
