import './Scroll.css';
import { ReactNode } from 'react';

type ScrollProps = {
  children: ReactNode;
};
const Scroll = (props: ScrollProps) => {
  return <div className="scroll-container">{props.children}</div>;
};
export default Scroll;
