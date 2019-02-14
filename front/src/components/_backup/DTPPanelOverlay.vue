<template>
  <div class="panel-with-overlay">
    <div class="main-content-area">
      <div class="filters">
        <div class="d-flex justify-content-between align-items-start flex-wrap map-stats-switcher">
          <button class="btn mr-2 mb-1 active">
            <i class="fa fa-map-o" aria-hidden="true"></i>&nbsp;Карта
          </button>
          <button class="btn">
            <i class="fa fa-bar-chart" aria-hidden="true"></i>&nbsp;Статистика
          </button>
        </div>
        <div class="map-legend">
          <span>Щелкните на кружок на карте, чтобы посмотреть подробности</span>
          <dtp-mvctype-checkbox type="auto" label="автомобили"></dtp-mvctype-checkbox>
          <dtp-mvctype-checkbox type="pedestrian" label="пешеходы"></dtp-mvctype-checkbox>
          <dtp-mvctype-checkbox type="bicycle" label="велосипедисты"></dtp-mvctype-checkbox>
        </div>
      </div>
    </div>
  </div>

  <!-- <div class="CheckBox" id="checkbox-div-onlyDead">
            <input id="checkbox-onlyDead" type="checkbox" value="false">
            <span class="fa fa-circle-o"></span> - только смертельные ДТП
          </div>
        </div>
      </div>
      <div class="filter-form">
        <div class="form-group">
          <label for="dateFilter">По дате</label>
          <input class="form-control date-filter" id="dateFilter" type="text">
        </div>
        <div class="form-group">
          <label for="typeFilter">По типу</label>
          <div class="filter-select">
            <div class="Select has-value is-clearable is-searchable Select--single">
              <div class="Select-control">
                <span class="Select-multi-value-wrapper" id="react-select-2--value">
                  <div class="Select-value">
                    <span
                      class="Select-value-label"
                      role="option"
                      aria-selected="true"
                      id="react-select-2--value-item"
                    >Все</span>
                  </div>
                  <div class="Select-input" style="display: inline-block;">
                    <input
                      id="typeFilter"
                      aria-activedescendant="react-select-2--value"
                      aria-expanded="false"
                      aria-haspopup="false"
                      aria-owns
                      role="combobox"
                      value
                      style="box-sizing: content-box; width: 5px;"
                    >
                    <div
                      style="position: absolute; top: 0px; left: 0px; visibility: hidden; height: 0px; overflow: scroll; white-space: pre; font-size: 14px; font-family: Arial, sans-serif; font-weight: 400; font-style: normal; letter-spacing: normal; text-transform: none;"
                    ></div>
                  </div>
                </span>
                <span aria-label="Очистить" class="Select-clear-zone" title="Очистить">
                  <span class="Select-clear">×</span>
                </span>
                <span class="Select-arrow-zone">
                  <span class="Select-arrow"></span>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label for="offenceFilter">По нарушению ПДД</label>
          <div class="filter-select">
            <div class="Select has-value is-clearable is-searchable Select--single">
              <div class="Select-control">
                <span class="Select-multi-value-wrapper" id="react-select-3--value">
                  <div class="Select-value">
                    <span
                      class="Select-value-label"
                      role="option"
                      aria-selected="true"
                      id="react-select-3--value-item"
                    >Любое</span>
                  </div>
                  <div class="Select-input" style="display: inline-block;">
                    <input
                      id="offenceFilter"
                      aria-activedescendant="react-select-3--value"
                      aria-expanded="false"
                      aria-haspopup="false"
                      aria-owns
                      role="combobox"
                      value
                      style="box-sizing: content-box; width: 5px;"
                    >
                    <div
                      style="position: absolute; top: 0px; left: 0px; visibility: hidden; height: 0px; overflow: scroll; white-space: pre; font-size: 14px; font-family: Arial, sans-serif; font-weight: 400; font-style: normal; letter-spacing: normal; text-transform: none;"
                    ></div>
                  </div>
                </span>
                <span aria-label="Очистить" class="Select-clear-zone" title="Очистить">
                  <span class="Select-clear">×</span>
                </span>
                <span class="Select-arrow-zone">
                  <span class="Select-arrow"></span>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label for="streetFilter">Улица</label>
          <div class="filter-select">
            <div class="Select has-value is-clearable is-searchable Select--single">
              <div class="Select-control">
                <span class="Select-multi-value-wrapper" id="react-select-4--value">
                  <div class="Select-value">
                    <span
                      class="Select-value-label"
                      role="option"
                      aria-selected="true"
                      id="react-select-4--value-item"
                    >Все</span>
                  </div>
                  <div class="Select-input" style="display: inline-block;">
                    <input
                      id="streetFilter"
                      aria-activedescendant="react-select-4--value"
                      aria-expanded="false"
                      aria-haspopup="false"
                      aria-owns
                      role="combobox"
                      value
                      style="box-sizing: content-box; width: 5px;"
                    >
                    <div
                      style="position: absolute; top: 0px; left: 0px; visibility: hidden; height: 0px; overflow: scroll; white-space: pre; font-size: 14px; font-family: Arial, sans-serif; font-weight: 400; font-style: normal; letter-spacing: normal; text-transform: none;"
                    ></div>
                  </div>
                </span>
                <span aria-label="Очистить" class="Select-clear-zone" title="Очистить">
                  <span class="Select-clear">×</span>
                </span>
                <span class="Select-arrow-zone">
                  <span class="Select-arrow"></span>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label for="nearbyFilter">Место поблизости</label>
          <div class="filter-select">
            <div class="Select has-value is-clearable is-searchable Select--single">
              <div class="Select-control">
                <span class="Select-multi-value-wrapper" id="react-select-5--value">
                  <div class="Select-value">
                    <span
                      class="Select-value-label"
                      role="option"
                      aria-selected="true"
                      id="react-select-5--value-item"
                    >Все</span>
                  </div>
                  <div class="Select-input" style="display: inline-block;">
                    <input
                      id="nearbyFilter"
                      aria-activedescendant="react-select-5--value"
                      aria-expanded="false"
                      aria-haspopup="false"
                      aria-owns
                      role="combobox"
                      value
                      style="box-sizing: content-box; width: 5px;"
                    >
                    <div
                      style="position: absolute; top: 0px; left: 0px; visibility: hidden; height: 0px; overflow: scroll; white-space: pre; font-size: 14px; font-family: Arial, sans-serif; font-weight: 400; font-style: normal; letter-spacing: normal; text-transform: none;"
                    ></div>
                  </div>
                </span>
                <span aria-label="Очистить" class="Select-clear-zone" title="Очистить">
                  <span class="Select-clear">×</span>
                </span>
                <span class="Select-arrow-zone">
                  <span class="Select-arrow"></span>
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="form-group">
          <label>Загрузить маркеры на карту</label>
          <div id="file-markersInput">
            <input
              class="form-control form-control-sm"
              id="file-markersInput"
              accept=".txt, .json"
              type="file"
            >
          </div>
        </div>
      </div>
      <p class="legend-text">Координаты некоторых ДТП могут быть неточными.</p>
  </div>-->
  <!-- <div class="overlay-area">
      <dtp-mvc-detail></dtp-mvc-detail>
  </div>-->
  <!-- </div> -->
</template>

<script>
import DTPMvcDetail from "@/components/DTPMvcDetail";
import DTPMVCTypeCheckbox from "@/components/DTPMVCTypeCheckbox";
export default {
  name: "dtp-panel-overlay",
  components: {
    "dtp-mvc-detail": DTPMvcDetail,
    "dtp-mvctype-checkbox": DTPMVCTypeCheckbox
  }
};
</script>
