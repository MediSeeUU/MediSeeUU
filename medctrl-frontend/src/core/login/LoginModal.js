import React, { useState } from 'react'
import ReactModal from 'react-modal'
import NavLink from '../navigation/NavComponents/NavLink'
import LoginForm from './LoginForm'
import './LoginModal.css'

// function based component representing the login button inserted into navbar
function LoginModal(props) {
  const [showModal, setModalState] = useState(false)

  return (
    <>
      <NavLink
        name="Login"
        image="bx bx-log-in"
        dest="#"
        parent={props.parent}
        lowest={true}
        onClick={() => setModalState(true)}
      />

      <ReactModal
        className="menu-modal"
        isOpen={showModal}
        onRequestClose={() => setModalState(false)}
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
        <LoginForm onClose={() => setModalState(false)} parent={props.parent} />
      </ReactModal>
    </>
  )
}

export default LoginModal
