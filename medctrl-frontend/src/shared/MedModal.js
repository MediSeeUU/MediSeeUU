import ReactModal from 'react-modal'

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
