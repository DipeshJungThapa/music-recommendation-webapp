import { ReactNode } from 'react';
import './Card.css';
type CardProps = {
  children: ReactNode;
  className: string;
};
const Card = ({ children, className }: CardProps) => {
  return <div className={`card ${className}`}>{children}</div>;
};
export default Card;
