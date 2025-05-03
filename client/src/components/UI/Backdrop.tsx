import ReactDOM from 'react-dom';
import './Backdrop.css';

type BackdropProps = {
  onClick: () => void;
};
const Backdrop = (props: BackdropProps) => {
  return ReactDOM.createPortal(
    <div className="backdrop" onClick={props.onClick}></div>,
    document.getElementById('backdrop-hook')!
  );
};

export default Backdrop;
