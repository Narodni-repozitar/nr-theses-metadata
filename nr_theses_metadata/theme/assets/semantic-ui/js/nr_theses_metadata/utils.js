// This file is part of InvenioRDM
// Copyright (C) 2021 CERN.
// Copyright (C) 2021 New York University.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import axios from 'axios'
import _get from 'lodash/get'
import _isArray from 'lodash/isArray'
import { DateTime } from 'luxon'
import React from 'react'
import { i18next } from '@translations/nr_theses_metadata/i18next'
import { ValueSeparator } from './components/ValueSeparator'

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

export function SearchItemLanguages({ languages }) {
  return
}

export function SearchItemCreatibutors({ creators }) {
  function getIcon(creator) {
    let ids = _get(creator, 'identifiers', [])
    let creatorName = _get(creator, 'fullName', 'No name')
    let firstId = ids.filter((id) => ['orcid', 'ror'].includes(id.scheme))[0]
    firstId = firstId || { scheme: '' }
    let icon = null
    switch (firstId.scheme) {
      case 'orcid':
        icon = (
          <a
            className="identifier-link"
            href={'https://orcid.org/' + `${firstId.identifier}`}
            aria-label={`${creatorName}: ${i18next.t('ORCID profile')}`}
            title={`${creatorName}: ${i18next.t('ORCID profile')}`}
          >
            <img
              className="inline-id-icon"
              src="/static/images/orcid.svg"
              alt=""
            />
          </a>
        )
        break
      case 'ror':
        icon = (
          <a
            href={'https://ror.org/' + `${firstId.identifier}`}
            aria-label={`${creatorName}: ${i18next.t('ROR profile')}`}
            title={`${creatorName}: ${i18next.t('ROR profile')}`}
          >
            <img
              className="inline-id-icon"
              src="/static/images/ror-icon.svg"
              alt=""
            />
          </a>
        )
        break
      default:
        break
    }
    return icon
  }

  function getLink(creator) {
    let creatorName = _get(creator, 'fullName', 'No name')
    let link = (
      <a
        className="creatibutor-link"
        href={`/search?q=metadata.creators.fullName:"${creatorName}"`}
        title={`${creatorName}: ${i18next.t('Search')}`}
      >
        <span className="creatibutor-name">{creatorName}</span>
      </a>
    )
    return link
  }
  return creators.map((creator, index) => (
    <span className="creatibutor-wrap" key={index}>
      {getLink(creator)}
      {getIcon(creator)}
      {index < creators.length - 1 && <ValueSeparator></ValueSeparator>}
    </span>
  ))
}

export function localizedSubjects(result) {
  const lang = i18next.language.toString()
  const subjects = _get(result, 'ui.subjects', []).map((s) => s.subject)
  return subjects.map((s) => {
    const match = s.filter((ss) => ss.lang === lang)
    if (!match.length && s.length > 0) {
      return s[0]
    }
    return match[0]
  })
}

export function localizedDescription(result) {
  const lang = i18next.language.toString()
  const description = _get(result, 'ui.abstract', 'No description')
  let description_localized = description
  if (_isArray(description)) {
    description_localized = description
      .filter((d) => d.lang === lang)
      .map((d) => d.value)

    if (!description_localized.length && description.length > 0) {
      description_localized = description[0].value
    }
  }
  return description_localized
}
