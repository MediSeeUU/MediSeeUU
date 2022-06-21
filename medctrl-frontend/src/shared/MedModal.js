// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import ReactModal from 'react-modal'

// Function based component that renders a modal
export default function MedModal({
  children,
  showModal,
  closeModal,
  className,
}) {
  return (
    <ReactModal
      className={className || 'med-modal'}
      isOpen={showModal}
      onRequestClose={closeModal}
      ariaHideApp={false}
      style={{
        modal: {},
        overlay: {
          background: 'rgba(0, 0, 0, 0.2)',
          backdropFilter: 'blur(2px)',
        },
      }}
    >
      {children}
    </ReactModal>
  )
}
