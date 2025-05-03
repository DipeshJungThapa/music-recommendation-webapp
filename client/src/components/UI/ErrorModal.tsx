import Modal from './Modal';
import './ErrorModal.css';
import Button from './Button.tsx';

type ErrorModalProps = {
  onClear: () => void;
  error: string;
};
const ErrorModal = (props: ErrorModalProps) => {
  return (
    <Modal
      onCancel={props.onClear}
      header="An Error Occurred!"
      show={!!props.error}
      footer={<Button onClick={props.onClear}>Okay</Button>}
    >
      <p>{props.error}</p>
    </Modal>
  );
};
export default ErrorModal;
