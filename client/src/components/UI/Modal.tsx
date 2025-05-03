import React, { ReactNode } from 'react';
import ReactDOM from 'react-dom';
import { CSSTransition } from 'react-transition-group';
import Backdrop from './Backdrop';
import './Modal.css';

type ModalOverlayProps = {
  className?: string;
  style?: React.CSSProperties;
  headerClass?: string;
  header: string;
  contentClass?: string;
  footerClass?: string;
  children: ReactNode;
  onSubmit?: (event: React.FormEvent) => void;
  footer: ReactNode;
};

const ModalOverlay: React.FC<ModalOverlayProps> = (props) => {
  const content = (
    <div className={`modal ${props.className}`} style={props.style}>
      <header className={`modal__header ${props.headerClass}`}>
        <h2>{props.header}</h2>
      </header>
      <form
        onSubmit={
          props.onSubmit ? props.onSubmit : (event) => event.preventDefault()
        }
      >
        <div className={`modal__content ${props.contentClass}`}>
          {props.children}
        </div>
        <footer className={`modal__footer ${props.footerClass}`}>
          {props.footer}
        </footer>
      </form>
    </div>
  );

  return ReactDOM.createPortal(
    content,
    document.getElementById('modal-hook') as HTMLElement
  );
};

type ModalProps = {
  show: boolean;
  onCancel: () => void;
  onSubmit?: (event: React.FormEvent) => void;
  header: string;
  footer: ReactNode;
  className?: string;
  style?: React.CSSProperties;
  headerClass?: string;
  contentClass?: string;
  footerClass?: string;
  children: ReactNode;
};

const Modal: React.FC<ModalProps> = (props) => {
  return (
    <React.Fragment>
      {props.show && <Backdrop onClick={props.onCancel} />}
      <CSSTransition
        in={props.show}
        mountOnEnter
        unmountOnExit
        timeout={200}
        classNames="modal"
      >
        <ModalOverlay {...props}>{props.children}</ModalOverlay>
      </CSSTransition>
    </React.Fragment>
  );
};

export default Modal;
