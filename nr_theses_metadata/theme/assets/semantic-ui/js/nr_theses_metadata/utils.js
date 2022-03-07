// This file is part of InvenioRDM
// Copyright (C) 2021 CERN.
// Copyright (C) 2021 New York University.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import axios from 'axios'
import _get from 'lodash/get'
import { DateTime } from 'luxon'
/**
 * Wrap a promise to be cancellable and avoid potential memory leaks
 * https://reactjs.org/blog/2015/12/16/ismounted-antipattern.html
 * @param promise the promise to wrap
 * @returns {Object} an object containing the promise to resolve and a `cancel` fn to reject the promise
 */
export const withCancel = (promise) => {
  let isCancelled = false

  const wrappedPromise = new Promise((resolve, reject) => {
    promise.then(
      (val) => (isCancelled ? reject('UNMOUNTED') : resolve(val)),
      (error) => (isCancelled ? reject('UNMOUNTED') : reject(error)),
    )
  })

  return {
    promise: wrappedPromise,
    cancel() {
      isCancelled = true
    },
  }
}

const apiConfig = {
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
}

export const axiosWithconfig = axios.create(apiConfig)

/**
 * Returns a human readable timestamp in the format "4 days ago".
 *
 * @param {Date} timestamp
 * @returns string
 */
export const timestampToRelativeTime = (timestamp) =>
  DateTime.fromISO(timestamp).toRelative()
