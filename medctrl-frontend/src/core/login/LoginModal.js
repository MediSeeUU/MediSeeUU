import React, { useState } from 'react'
import ReactModal from 'react-modal'
import NavLink from '../navigation/NavComponents/NavLink'
import LoginForm from './LoginForm'
import './LoginModal.css'

// function based component representing the login button inserted into navbar
function LoginModal(props) {
  const [showModal, setModalState] = useState(false)

  const closeModal = () => setModalState(false)
  const openModal = () => setModalState(true)

  return (
    <>
      <NavLink
        tour='step-nav-login'
        name="Login"
        image="bx bx-log-in"
        dest="#"
        parent={props.parent}
        lowest={true}
        onClick={openModal}
      />

      <ReactModal
        className="menu-modal"
        isOpen={showModal}
        onRequestClose={closeModal}
        ariaHideApp={false}
        style={{
          modal: {},
          overlay: {
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(2px)',
          },
          content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
          },
        }}
      >
        <LoginForm onClose={closeModal} parent={props.parent} />
      </ReactModal>
    </>
  )
}

export default LoginModal
