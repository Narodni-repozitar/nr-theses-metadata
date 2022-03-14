// This file is part of InvenioRDM
// Copyright (C) 2021 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from 'react'
import PropTypes from 'prop-types'

export class ValueSeparator extends Component {
  render() {
    const { double } = this.props
    return (
      <div className="value-separator">
        <div className="vertical-bar"></div>
        {double && <div className="vertical-bar"></div>}
      </div>
    )
  }
}

ValueSeparator.propTypes = {
  double: PropTypes.bool,
}

ValueSeparator.defaultProps = {
  double: false,
}
