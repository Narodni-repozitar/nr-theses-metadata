// This file is part of InvenioRDM
// Copyright (C) 2020 CERN.
// Copyright (C) 2020 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import React, { Component } from 'react'
import { withState } from 'react-searchkit'
import { createSearchAppInit, defaultComponents } from '@js/invenio_search_ui'
import {
  NRBucketAggregationElement,
  NRRecordFacets,
  NRRecordFacetsValues,
  NRResultsGridItem,
  NRResultsListItem,
  NRRecordSearchBarContainer,
  NRRecordSearchBarElement,
  NRCountComponent,
  NREmptyResults,
  NRErrorComponent,
  NRToggleComponent,
  NRBucketAggregationsModal,
  NRBucketAggregationsValuesModal,
  NRBucketContainerElementModal,
} from './components'

class _StateLogger extends Component {
  render() {
    return (
      <div>
        Current results state{' '}
        <pre>{JSON.stringify(this.props.currentResultsState, null, 2)}</pre>
      </div>
    )
  }
}

const renderResultsList = (results) => {
  const State = withState(_StateLogger)
  console.log(results)
  return <State></State>
}

const initSearchApp = createSearchAppInit({
  'BucketAggregation.element': NRBucketAggregationElement,
  'BucketAggregationValues.element': NRRecordFacetsValues,
  'ResultsGrid.item': NRResultsGridItem,
  'EmptyResults.element': NREmptyResults,
  'BucketAggregation.element.modal': NRBucketAggregationsModal,
  'BucketAggregationValues.element.modal': NRBucketAggregationsValuesModal,
  'BucketAggregationContainer.element.modal': NRBucketContainerElementModal,
  // ResultsList: renderResultsList,
  'ResultsList.item': NRResultsListItem,
  'SearchApp.facets': NRRecordFacets,
  'SearchApp.searchbarContainer': NRRecordSearchBarContainer,
  'SearchBar.element': NRRecordSearchBarElement,
  'Count.element': NRCountComponent,
  'Error.element': NRErrorComponent,
  'SearchFilters.ToggleComponent': NRToggleComponent,
})
