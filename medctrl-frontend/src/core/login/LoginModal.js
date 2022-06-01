import React, { useState } from 'react'
import ReactModal from 'react-modal'
import MedModal from '../../shared/MedModal/MedModal'
import NavLink from '../navigation/NavComponents/NavLink'
import LoginForm from './LoginForm'
import './LoginModal.css'

// Function based component representing the login button inserted into the navigation bar
function LoginModal(props) {
  const [showModal, setModalState] = useState(false)

  const closeModal = () => setModalState(false)
  const openModal = () => setModalState(true)

  return (
    <>
      <NavLink
        tour="step-nav-login"
        name="Login"
        image="bx bx-log-in"
        dest="#"
        parent={props.parent}
        lowest={true}
        onClick={openModal}
      />

      <MedModal showModal={showModal} closeModal={closeModal}>
        <LoginForm onClose={closeModal} parent={props.parent} />
      </MedModal>
    </>
  )
}

export default LoginModal
