import './LoadingSpinner.css';

type LoadingSpinnerProps = {
  asOverlay?: boolean;
};

const LoadingSpinner = ({ asOverlay }: LoadingSpinnerProps) => {
  return (
    <div className={`${asOverlay ? 'loading-spinner__overlay' : ''}`}>
      <div className="lds-dual-ring"></div>
    </div>
  );
};

export default LoadingSpinner;
