import React from "react";
import * as PropTypes from "prop-types";

function getValue(dictionary, key, default_val) {
    let result = dictionary[key];
    if (typeof result === "undefined") {
        result = default_val;
    }
    return result;
}

export class PhotoViewer extends React.Component {
    constructor(props) {
        super(props);
    }

    getSource (photoData, displaySide="photo") {
        photoData.propTypes = {
            map_square_number: PropTypes.object
        };
        return `${this.props.photoDir}/${photoData.map_square_number}/${photoData.number}_${displaySide}.jpg`;
    };

    getPhotoGrid (photoData, config={}) {
        const className = getValue(config, "className", "");
        const photoSize = getValue(config, "photoSize", [100, 100]);
        const titleFunc = getValue(
            config,
            "titleFunc",
            (k, photo) => `Map Square: ${photo["map_square_number"]}` +
                                        `, Photo: ${photo["number"]}`
        );
        const hrefFunc = getValue(
            config,
            "hrefFunc",
            (k, photo) => `/photo/${photo["map_square_number"]}/${photo["number"]}/`
        );
        const onClickFunc = getValue(config, "onClickFunc", (_k, _photo) => () => {});
        return photoData.map((photo, k) => {
            return (
                <a
                    key={k}
                    className={className}
                    title={titleFunc(k, photo)}
                    href={hrefFunc(k, photo)}
                    onClick={onClickFunc(k, photo)}>
                    <img
                        alt={photo.alt}
                        width={photoSize[0]}
                        height={photoSize[1]}
                        src={this.getSource(photo)}
                    />
                </a>
            );
        });
    }

    getPhotoSlider(photoData, config={}) {
        // TODO: Disable scroll buttons when there are no more photos to scroll through
        return (
            <div className="photos-box">
                <button
                    type="button"
                    className="slider-scroll-left btn btn-dark"
                    onClick={
                    () => document.getElementById("photo-slider").scrollLeft -=
                        document.getElementById("photo-slider").clientWidth}
                >&#8249;</button>
                <div id="photo-slider" className="slider-photos">
                    {this.getPhotoGrid(photoData, config)}
                </div>
                <button
                    type="button"
                    className="slider-scroll-right btn btn-dark"
                    onClick={
                    () => document.getElementById("photo-slider").scrollLeft +=
                        document.getElementById("photo-slider").clientWidth}
                >&#8250;</button>
            </div>
        );
    }
}

PhotoViewer.propTypes = {
    photoDir: PropTypes.string
};

export default PhotoViewer;
