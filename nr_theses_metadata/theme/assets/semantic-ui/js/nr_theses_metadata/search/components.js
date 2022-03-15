// This file is part of InvenioRDM
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2021-2022 New York University.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import React, { Fragment, useState } from 'react'
import {
  Button,
  Card,
  Checkbox,
  Grid,
  Header,
  Icon,
  Input,
  Item,
  Label,
  List,
  Message,
  Segment,
} from 'semantic-ui-react'
import { BucketAggregation, withState } from 'react-searchkit'
import _get from 'lodash/get'
import _capitalize from 'lodash/capitalize'
import _truncate from 'lodash/truncate'
import Overridable from 'react-overridable'
import { SearchBar } from '@js/invenio_search_ui/components'
import { i18next } from '@translations/nr_theses_metadata/i18next'
import {
  localizedDescription,
  localizedSubjects,
  SearchItemCreatibutors,
  SearchItemLanguages,
} from '../utils'
import { ValueSeparator } from '../components/ValueSeparator'

export const NRResultsListItem = ({ result, index }) => {
  const access_rights = _get(result, 'ui.accessRights', 'open')
  let access_rights_class = 'open'
  let access_rights_icon = 'unlock'

  switch (access_rights) {
    case 'odložené zpřístupnění':
      access_rights_class = 'embargoed'
      access_rights_icon = 'outline clock'
      break
    case 'omezený přístup':
      access_rights_class = 'restricted'
      access_rights_icon = 'ban'
      break
    case 'pouze metadata':
      access_rights_class = 'metadata-only'
      access_rights_icon = 'tag'
      break
  }
  const access_status = _capitalize(access_rights)
  const access_status_icon = 'unlock'
  const creators = result.ui.creators.slice(0, 3)
  const contributors = result.ui.contributors?.slice(0, 3)

  const languages = _get(result, 'ui.languages')

  const publicationDate = _get(
    result,
    'ui.dateIssued',
    'No publication date found.',
  )
  const resource_type = _get(result, 'ui.resourceType', 'No resource type')

  const title = _get(result, 'metadata.title', 'No title')
  const version = _get(result, 'ui.version', null)

  const nuslIDs = _get(result, 'metadata.systemIdentifiers', [])
    .filter((id) => id.scheme === 'nusl')
    .map((id) => {
      return {
        uri: id.identifier,
        label: id.identifier.split('/').reverse()[0],
      }
    })

  // Derivatives
  // TODO: pass detail route from template context
  const viewLink = `/documents/${result.id}`
  return (
    <Item key={index}>
      <Item.Content>
        <Item.Extra className="labels-actions">
          <Label size="tiny" title={i18next.t('Publication date')} color="blue">
            {publicationDate} {version && <Fragment>({version})</Fragment>}
          </Label>
          <Label size="tiny" title={i18next.t('Resource type')} color="grey">
            {resource_type}
          </Label>
          <Label
            size="tiny"
            title={i18next.t('Access status')}
            className={`access-status ${access_rights_class}`}
          >
            {access_status_icon && (
              <i className={`icon ${access_rights_icon}`} />
            )}
            {access_status}
          </Label>
          {languages.map((lang, index) => (
            <Label
              size="tiny"
              title={i18next.t('Languages')}
              color="green"
              basic
              key={index}
            >
              {lang.toUpperCase()}
            </Label>
          ))}
          {nuslIDs.map((nid) => (
            <Label
              basic
              title={i18next.t('Original NUSL identifier')}
              size="tiny"
              key={nid.uri}
            >
              <a target="_blank" href={nid.uri}>
                {nid.label}
              </a>
            </Label>
          ))}
        </Item.Extra>
        <Item.Header as="h2">
          <a href={viewLink}>{title}</a>
        </Item.Header>
        <Item.Meta
          title={i18next.t('Creators and contributors')}
          className="creatibutors creatibutor-list"
        >
          <SearchItemCreatibutors creators={creators} />
          {contributors && (
            <Fragment>
              <ValueSeparator double></ValueSeparator>
              <SearchItemCreatibutors creators={contributors} />
            </Fragment>
          )}
        </Item.Meta>
        <Item.Description>
          {_truncate(localizedDescription(result), { length: 350 })}
        </Item.Description>
        <Item.Extra title={i18next.t('Subjects')}>
          {localizedSubjects(result).map((subject, index) => (
            <Label
              style={{ opacity: 0.6 }}
              color="green"
              image
              key={index}
              size="tiny"
            >
              {subject.lang.toUpperCase()}
              <Label.Detail className="item-subject-detail">
                {_truncate(subject.value, { length: 100 })}
              </Label.Detail>
            </Label>
          ))}
        </Item.Extra>
      </Item.Content>
    </Item>
  )
}

// TODO: Update this according to the full List item template?
export const NRResultsGridItem = ({ result, index }) => {
  return (
    // TODO: pass detail route from template context
    <Card fluid key={index} href={`/documents/${result.pid}`}>
      <Card.Content>
        <Card.Header>{result.metadata.title}</Card.Header>
        <Card.Description>
          {_truncate(localizedDescription(result), { length: 200 })}
        </Card.Description>
      </Card.Content>
    </Card>
  )
}

export const NRRecordSearchBarContainer = () => {
  return (
    <Overridable id={'SearchApp.searchbar'}>
      <SearchBar />
    </Overridable>
  )
}

export const NRRecordSearchBarElement = withState(
  ({
    placeholder: passedPlaceholder,
    queryString,
    onInputChange,
    executeSearch,
    updateQueryState,
  }) => {
    const placeholder = passedPlaceholder || i18next.t('Search')
    const onBtnSearchClick = () => {
      updateQueryState({ filters: [] })
      executeSearch()
    }
    const onKeyPress = (event) => {
      if (event.key === 'Enter') {
        updateQueryState({ filters: [] })
        executeSearch()
      }
    }
    return (
      <Input
        action={{
          icon: 'search',
          onClick: onBtnSearchClick,
          className: 'search',
          'aria-label': 'Search',
        }}
        fluid
        placeholder={placeholder}
        onChange={(event, { value }) => {
          onInputChange(value)
        }}
        value={queryString}
        onKeyPress={onKeyPress}
      />
    )
  },
)

export const NRRecordFacetsValues = ({
  bucket,
  isSelected,
  onFilterClicked,
  getChildAggCmps,
}) => {
  const childAggCmps = getChildAggCmps(bucket)
  const [isActive, setisActive] = useState(false)
  const hasChildren = childAggCmps && childAggCmps.props.buckets.length > 0
  const keyField = bucket.key_as_string ? bucket.key_as_string : bucket.key
  return (
    <List.Item key={bucket.key}>
      <div
        className={`facet-wrapper title ${
          hasChildren ? '' : 'facet-subtitle'
        } ${isActive ? 'active' : ''}`}
      >
        <List.Content className="facet-count">
          <Label circular id={`${keyField}-count`}>
            {bucket.doc_count}
          </Label>
        </List.Content>
        {hasChildren ? (
          <Button
            className="iconhold"
            icon={`angle ${isActive ? 'down' : 'right'} icon`}
            onClick={() => setisActive(!isActive)}
            aria-label={`${
              isActive
                ? i18next.t('hide subfacets')
                : i18next.t('show subfacets')
            }`}
          />
        ) : null}
        <Checkbox
          label={bucket.label || keyField}
          id={`${keyField}-facet-checkbox`}
          aria-describedby={`${keyField}-count`}
          value={keyField}
          onClick={() => onFilterClicked(keyField)}
          checked={isSelected}
        />
      </div>
      <div className={`content facet-content ${isActive ? 'active' : ''}`}>
        {childAggCmps}
      </div>
    </List.Item>
  )
}

export const SearchHelpLinks = () => {
  return (
    <Overridable id={'RdmSearch.SearchHelpLinks'}>
      <List>
        <List.Item>
          <a href="/help/search">{i18next.t('Search guide')}</a>
        </List.Item>
      </List>
    </Overridable>
  )
}

export const NRRecordFacets = ({ aggs, currentResultsState }) => {
  return (
    <aside aria-label={i18next.t('filters')} id="search-filters">
      {aggs.map((agg, index) => {
        return (
          <div className="ui accordion" key={`${agg.title}-${index}`}>
            <BucketAggregation title={agg.title} agg={agg} />
          </div>
        )
      })}
      <Card className="borderless-facet">
        <Card.Content>
          <Card.Header as="h2">{i18next.t('Help')}</Card.Header>
          <SearchHelpLinks />
        </Card.Content>
      </Card>
    </aside>
  )
}

export const NRBucketAggregationElement = ({
  agg,
  title,
  containerCmp,
  updateQueryFilters,
}) => {
  const clearFacets = () => {
    if (containerCmp.props.selectedFilters.length) {
      updateQueryFilters([agg.aggName, ''], containerCmp.props.selectedFilters)
    }
  }

  const hasSelections = () => {
    return !!containerCmp.props.selectedFilters.length
  }

  return (
    <Card className="borderless-facet">
      <Card.Content>
        <Card.Header as="h2">
          {title}
          <Button
            basic
            icon
            size="mini"
            floated="right"
            onClick={clearFacets}
            aria-label={i18next.t('Clear selection')}
            title={i18next.t('Clear selection')}
            disabled={!hasSelections()}
          >
            {i18next.t('Clear')}
          </Button>
        </Card.Header>
      </Card.Content>
      <Card.Content>{containerCmp}</Card.Content>
    </Card>
  )
}

export const NRToggleComponent = ({
  updateQueryFilters,
  userSelectionFilters,
  filterValue,
  label,
  title,
  isChecked,
}) => {
  const _isChecked = (userSelectionFilters) => {
    const isFilterActive =
      userSelectionFilters.filter((filter) => filter[0] === filterValue[0])
        .length > 0
    return isFilterActive
  }

  const onToggleClicked = () => {
    updateQueryFilters(filterValue)
  }

  var isChecked = _isChecked(userSelectionFilters)
  return (
    <Card className="borderless-facet">
      <Card.Content>
        <Card.Header as="h2">{title}</Card.Header>
      </Card.Content>
      <Card.Content>
        <Checkbox
          toggle
          label={label}
          name="versions-toggle"
          id="versions-toggle"
          onClick={onToggleClicked}
          checked={isChecked}
        />
      </Card.Content>
    </Card>
  )
}

export const NRCountComponent = ({ totalResults }) => {
  return <Label>{totalResults.toLocaleString()}</Label>
}

export const NREmptyResults = (props) => {
  const queryString = props.queryString
  const searchPath = props.searchPath || '/search'

  return (
    <Grid>
      <Grid.Row centered>
        <Grid.Column width={12} textAlign="center">
          <Header as="h2">
            {i18next.t("We couldn't find any matches for ")}
            {(queryString && `'${queryString}'`) || i18next.t('your search')}
          </Header>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row centered>
        <Grid.Column width={8} textAlign="center">
          <Button primary onClick={props.resetQuery}>
            <Icon name="search" />
            {i18next.t('Start over')}
          </Button>
        </Grid.Column>
      </Grid.Row>
      <Grid.Row centered>
        <Grid.Column width={12}>
          <Segment secondary padded size="large">
            <Header as="h3" size="small">
              {i18next.t('ProTip')}!
            </Header>
            <p>
              <a
                href={`${searchPath}?q=metadata.publication_date:[2017-01-01 TO *]`}
              >
                metadata.publication_date:[2017-01-01 TO *]
              </a>{' '}
              {i18next.t(
                'will give you all the publications from 2017 until today',
              )}
              .
            </p>
            <p>
              {i18next.t('For more tips, check out our ')}
              <a href="/help/search" title={i18next.t('Search guide')}>
                {i18next.t('search guide')}
              </a>
              {i18next.t(' for defining advanced search queries')}.
            </p>
          </Segment>
        </Grid.Column>
      </Grid.Row>
    </Grid>
  )
}

export const NRErrorComponent = ({ error }) => {
  return (
    <Message warning>
      <Message.Header>
        <Icon name="warning sign" />
        {error.response.data.message}
      </Message.Header>
    </Message>
  )
}
