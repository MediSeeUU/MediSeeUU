// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import MedModal from '../../shared/MedModal'
import NavLink from '../navigation/components/NavLink'
import LoginForm from './LoginForm'
import './LoginModal.css'

// Function based component representing the login button inserted into the navigation bar
function LoginModal(props) {
  // Initialize modal state (by default false)
  const [showModal, setModalState] = useState(false)

  // Functions to open and close the modal
  const openModal = () => setModalState(true)
  const closeModal = () => setModalState(false)

  // Render the button on the navigation and the modal with the content of the LoginForm component
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
