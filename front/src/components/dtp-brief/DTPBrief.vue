<template>
  <div class="brief-stats-section">
    <div class="brief-stats">
      <table class="table table-borderless">
        <tbody>
          <tr>
            <td class="city-name align-middle"></td>
            <td class="align-middle text-center">
              Пострадавшие
              <b>{{injured}}</b>
            </td>
            <td class="align-middle text-center">
              Погибшие
              <b>{{dead}}</b>
            </td>
          </tr>

          <tr>
            <td>
              <span class="align-middle">Количество ДТП</span>
              <span class="mvc-count ml-2 align-middle">{{mvcCount}}</span>
            </td>

            <td>
              <div class="row justify-content-center">
                <div class="col-auto media align-items-center">
                  <img src="@/assets/driver.png">
                  <div class="media-body">{{injuredAuto}}</div>
                </div>

                <div class="col-auto media align-items-center">
                  <img src="@/assets/pedestrian.png">
                  <div class="media-body">{{injuredPedestrian}}</div>
                </div>

                <div class="col-auto media align-items-center">
                  <img src="@/assets/cyclist.png">
                  <div class="media-body">{{injuredBicycle}}</div>
                </div>
              </div>
            </td>

            <td>
              <div class="row justify-content-center">
                <div class="col-auto media align-items-center">
                  <img src="@/assets/driver.png">
                  <div class="media-body">{{deadAuto}}</div>
                </div>

                <div class="col-auto media align-items-center">
                  <img src="@/assets/pedestrian.png">
                  <div class="media-body">{{deadPedestrian}}</div>
                </div>

                <div class="col-auto media align-items-center">
                  <img src="@/assets/cyclist.png">
                  <div class="media-body">{{deadBicycle}}</div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>