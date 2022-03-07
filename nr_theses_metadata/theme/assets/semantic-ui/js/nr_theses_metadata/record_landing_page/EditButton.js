// This file is part of InvenioRDM
// Copyright (C) 2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { useState } from 'react'
import { Icon, Button } from 'semantic-ui-react'
import { i18next } from '@translations/nr_theses_metadata/i18next'
import { axiosWithconfig } from '../utils'

export const EditButton = (props) => {
  const [loading, setLoading] = useState(false)
  const recid = props.recid
  const handleError = props.onError
  const handleClick = () => {
    setLoading(true)
    axiosWithconfig
      // TODO: generate / put proper model url path for record submission
      .post(`/api/nr_theses_metadata/${recid}/draft`)
      .then((response) => {
        window.location = `/uploads/${recid}`
      })
      .catch((error) => {
        setLoading(false)
        handleError(error.response.data.message)
      })
  }

  return (
    <Button
      fluid
      color="orange"
      size="mini"
      onClick={handleClick}
      loading={loading}
    >
      <Icon name="edit" />
      {i18next.t('Edit')}
    </Button>
  )
}
