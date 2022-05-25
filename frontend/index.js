/*
 * The entrypoint for our application:
 * This module gets loaded into the DOM, and then it loads everything else.
 */
import React from 'react';
import ReactDOM from 'react-dom';

// process.env.BABEL_ENV = 'development';
// process.env.NODE_ENV = 'development';
import 'bootstrap/dist/css/bootstrap.min.css';

import { IndexView } from './src/index';
import { PhotoView } from './src/photoView/photoView';
import { SimilarityView } from './src/similarityView/similarityView';
import { PhotographerView } from './src/photographerView/photographerView';
import { MapSquareView } from './src/mapSquareView/mapSquareView';
import { AnalysisView } from './src/analysisView/analysisView';
import { AllAnalysisView } from './src/analysisView/allAnalysisView';
import { AllPhotosView } from './src/similarityView/allPhotosView';
import { ClusterView } from './src/clusterView/clusterView';
import { Search } from './src/search/search';
import About from './src/about/about';

// Import all styles
// import './src/UILibrary/styles.scss';

const COMPONENT_PROPS_RAW = document.getElementById('component_props').text;
const COMPONENT_NAME_RAW = document.getElementById('component_name').text;
const COMPONENT_PROPS = JSON.parse(COMPONENT_PROPS_RAW);
const COMPONENT_NAME = JSON.parse(COMPONENT_NAME_RAW);
const COMPONENTS = {
    IndexView,
    About,
    Search,
    PhotoView,
    SimilarityView,
    PhotographerView,
    MapSquareView,
    AllAnalysisView,
    AnalysisView,
    AllPhotosView,
    ClusterView,
};

const PreselectedComponent = COMPONENTS[COMPONENT_NAME || 'ErrorNotFoundComponent'];

ReactDOM.render(<PreselectedComponent {...COMPONENT_PROPS} />, document.getElementById('app_root'));
