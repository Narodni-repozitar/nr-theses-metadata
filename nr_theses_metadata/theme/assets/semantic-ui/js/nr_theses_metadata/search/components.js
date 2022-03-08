// This file is part of InvenioRDM
// Copyright (C) 2020-2022 CERN.
// Copyright (C) 2020-2021 Northwestern University.
// Copyright (C) 2021 Graz University of Technology.
// Copyright (C) 2021-2022 New York University.
//
// Invenio App RDM is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import React, {useState} from 'react'
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
import {BucketAggregation, Toggle, withState} from 'react-searchkit'
import _get from 'lodash/get'
import _isArray from 'lodash/isArray'
import _truncate from 'lodash/truncate'
import Overridable from 'react-overridable'
import {SearchBar} from '@js/invenio_search_ui/components'
import {i18next} from '@translations/nr_theses_metadata/i18next'
import {SearchItemCreators} from '../utils'


export const ResultsListItem = ({result, index}) => {
    const lang = i18next.language.toString()
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
    const access_status =
        access_rights[0].toUpperCase() + access_rights.substring(1)
    const access_status_icon = 'unlock'
    const createdDate = _get(result, 'ui.created', 'No creation date found.')
    const creators = result.ui.creators.slice(0, 3)

    const description = _get(result, 'ui.abstract', 'No description')
    let description_localized = description
    if (_isArray(description)) {
        description_localized = description.filter((d) => d.lang === lang).map(d => d.value)

        if (!description_localized.length && description.length > 0) {
            description_localized = description[0]
        }
    }

    const publicationDate = _get(
        result,
        'ui.dateIssued',
        'No publication date found.',
    )
    const resource_type = _get(result, 'ui.resourceType', 'No resource type')
    const subjects = _get(result, 'ui.subjects', []).map(s => s.subject)
    const subjects_localized = subjects.map(s => {
      const match = s.filter(ss => ss.lang === lang )
        if (!match.length && s.length > 0) {
            return s[0].value
        }
        return match[0].value
    })

    console.log(subjects_localized)
    const title = _get(result, 'metadata.title', 'No title')
    const version = _get(result, 'ui.version', null)

    // Derivatives
    // TODO: pass detail route from template context
    const viewLink = `/documents/${result.id}`
    return (
        <Item key={index}>
            <Item.Content>
                <Item.Extra className="labels-actions">
                    <Label size="tiny" color="blue">
                        {publicationDate} ({version})
                    </Label>
                    <Label size="tiny" color="grey">
                        {resource_type}
                    </Label>
                    <Label size="tiny" className={`access-status ${access_rights_class}`}>
                        {access_status_icon && (
                            <i className={`icon ${access_rights_icon}`}/>
                        )}
                        {access_status}
                    </Label>
                </Item.Extra>
                <Item.Header as="h2">
                    <a href={viewLink}>{title}</a>
                </Item.Header>
                <Item className="creatibutors">
                    <SearchItemCreators creators={creators}/>
                </Item>
                <Item.Description>
                    {_truncate(description_localized, {length: 350})}
                </Item.Description>
                <Item.Extra>
                    {subjects_localized.map((subject, index) => (
                        <Label key={index} size="tiny">
                            {subject}
                        </Label>
                    ))}
                    {createdDate && (
                        <div>
                            <small>
                                {i18next.t('Uploaded on')} <span>{createdDate}</span>
                            </small>
                        </div>
                    )}
                </Item.Extra>
            </Item.Content>
        </Item>
    )
}

// TODO: Update this according to the full List item template?
export const RDMRecordResultsGridItem = ({result, index}) => {
    const description_stripped = _get(
        result,
        'ui.description_stripped',
        'No description',
    )
    return (
        <Card fluid key={index} href={`/records/${result.pid}`}>
            <Card.Content>
                <Card.Header>{result.metadata.title}</Card.Header>
                <Card.Description>
                    {_truncate(description_stripped, {length: 200})}
                </Card.Description>
            </Card.Content>
        </Card>
    )
}

export const RDMRecordSearchBarContainer = () => {
    return (
        <Overridable id={'SearchApp.searchbar'}>
            <SearchBar/>
        </Overridable>
    )
}

export const RDMRecordSearchBarElement = withState(
    ({
         placeholder: passedPlaceholder,
         queryString,
         onInputChange,
         executeSearch,
         updateQueryState,
     }) => {
        const placeholder = passedPlaceholder || i18next.t('Search')
        const onBtnSearchClick = () => {
            updateQueryState({filters: []})
            executeSearch()
        }
        const onKeyPress = (event) => {
            if (event.key === 'Enter') {
                updateQueryState({filters: []})
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
                onChange={(event, {value}) => {
                    onInputChange(value)
                }}
                value={queryString}
                onKeyPress={onKeyPress}
            />
        )
    },
)

export const RDMRecordFacetsValues = ({
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

export const RDMRecordFacets = ({aggs, currentResultsState}) => {
    return (
        <aside aria-label={i18next.t('filters')} id="search-filters">
            <Toggle
                title={i18next.t('Versions')}
                label={i18next.t('View all versions')}
                filterValue={['allversions', 'true']}
            />
            {aggs.map((agg) => {
                return (
                    <div className="ui accordion" key={agg.title}>
                        <BucketAggregation title={agg.title} agg={agg}/>
                    </div>
                )
            })}
            <Card className="borderless-facet">
                <Card.Content>
                    <Card.Header as="h2">{i18next.t('Help')}</Card.Header>
                    <SearchHelpLinks/>
                </Card.Content>
            </Card>
        </aside>
    )
}

export const RDMBucketAggregationElement = ({
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

export const RDMToggleComponent = ({
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

export const RDMCountComponent = ({totalResults}) => {
    return <Label>{totalResults.toLocaleString('en-US')}</Label>
}

export const RDMEmptyResults = (props) => {
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
                        <Icon name="search"/>
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

export const RDMErrorComponent = ({error}) => {
    return (
        <Message warning>
            <Message.Header>
                <Icon name="warning sign"/>
                {error.response.data.message}
            </Message.Header>
        </Message>
    )
}
