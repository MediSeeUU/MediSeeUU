import React, { useState } from 'react'
import MedModal from '../../shared/MedModal'
import NavLink from '../navigation/Components/NavLink'
import LoginForm from './LoginForm'
import './LoginModal.css'

// Function based component representing the login button inserted into the navigation bar
function LoginModal(props) {
  // Initialize modal state
  const [showModal, setModalState] = useState(false)

  // Functions to open and close the modal
  const openModal = () => setModalState(true)
  const closeModal = () => setModalState(false)

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
