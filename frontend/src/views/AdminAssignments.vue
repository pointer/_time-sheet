<template>
  <div>
    <v-flex xs12 sm6 md4 text-xs-right mb-2 mt-2 pr-2>
      <v-dialog
        v-model="assignDialog"
        max-width="900px"
        content-class="dlgNewEditItem"
      >
        <template v-slot:activator="{ on }">
          <v-btn color="secondary" v-on="on" class="btnNewItem pr-4">
            <v-icon class="mr-2">mdi-plus</v-icon>
            {{ $t('dataTable.NEW_ITEM') }}
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>
          <v-card-text>
            <v-container grid-list-md>
              <v-layout wrap>
                <v-flex xs12 md6>
                  <v-autocomplete
                    v-model="assignSite"
                    :items="allSites"
                    dense
                    filled
                    :label="$t('assignments.headers.ASSIGN_SITE')"
                  >
                  </v-autocomplete>
                </v-flex>
                <v-flex xs12 md6>
                  <v-autocomplete
                    v-model="assignTask"
                    :items="allTasks"
                    dense
                    filled
                    :label="$t('assignments.headers.ASSIGN_TASK')"
                  >
                    <!-- HTML that describe how select should render selected items -->
                    <!-- <template v-slot:selection="data">
                        {{ data.item.name }}
                      </template> -->
                    <!-- HTML that describe how select should render items when the select is open -->
                    <!--    <template v-slot:item="data">
                        {{ data.item.name }}
                      </template> -->
                  </v-autocomplete>
                </v-flex>
                <v-flex xs12 md6>
                  <v-autocomplete
                    v-model="assignEquipment"
                    :items="allEquipments"
                    dense
                    filled
                    :label="$t('assignments.headers.ASSIGN_EQUIPMENT')"
                  ></v-autocomplete>
                </v-flex>
                <v-row justify="space-around" align="center">
                  <v-menu
                    ref="assignDateMenu"
                    :close-on-content-click="false"
                    v-model="assignDateMenu"
                    transition="scale-transition"
                    offset-y
                    :nudge-right="40"
                    max-width="500px"
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="assignDates"
                        label="Assign date"
                        prepend-icon="event"
                        readonly
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker v-model="assignDates" multiple>
                      <v-spacer></v-spacer>
                      <v-btn
                        text
                        color="primary"
                        @click="assignDateMenu = false"
                        >Cancel
                      </v-btn>
                      <v-btn
                        text
                        color="primary"
                        @click="$refs.assignDateMenu.save(assignDates)"
                        >OK
                      </v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-row>
                <v-row justify="space-around" align="center">
                  <v-col cols="11" sm="5">
                    <v-menu
                      ref="startTimeMenu"
                      v-model="startTimeMenu"
                      :return-value.sync="assignStartTime"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      transition="scale-transition"
                      offset-y
                      max-width="500px"
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on }">
                        <v-text-field
                          v-model="assignStartTime"
                          label="Start time"
                          prepend-icon="access_time"
                          readonly
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-time-picker
                        v-if="startTimeMenu"
                        v-model="assignStartTime"
                        :max="assignEndTime"
                        :landscape="$vuetify.breakpoint.mdAndUp"
                        format="24hr"
                      >
                        <v-spacer></v-spacer>
                        <v-btn
                          text
                          color="primary"
                          @click="startTimeMenu = false"
                        >
                          Cancel
                        </v-btn>
                        <v-btn
                          text
                          color="primary"
                          @click="$refs.startTimeMenu.save(assignStartTime)"
                        >
                          OK
                        </v-btn>
                      </v-time-picker>
                    </v-menu>
                  </v-col>
                  <v-col cols="11" sm="5">
                    <v-menu
                      ref="endTimeMenu"
                      v-model="endTimeMenu"
                      :return-value.sync="assignEndTime"
                      :close-on-content-click="false"
                      :nudge-right="40"
                      transition="scale-transition"
                      offset-y
                      max-width="500px"
                      min-width="290px"
                    >
                      <template v-slot:activator="{ on }">
                        <v-text-field
                          v-model="assignEndTime"
                          label="End time"
                          prepend-icon="access_time"
                          readonly
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-time-picker
                        v-model="assignEndTime"
                        :min="assignStartTime"
                        :landscape="$vuetify.breakpoint.mdAndUp"
                        format="24hr"
                      >
                        <v-spacer></v-spacer>
                        <v-btn text color="primary" @click="endTimeMenu = false"
                          >Cancel</v-btn
                        >
                        <v-btn
                          text
                          color="primary"
                          @click="$refs.endTimeMenu.save(assignEndTime)"
                          >OK</v-btn
                        >
                      </v-time-picker>
                    </v-menu>
                  </v-col>
                </v-row>
                <v-row>
                  <template>
                    <v-container class="dark">
                      <v-row no-gutters>
                        <template>
                          <v-col>
                            <v-card class="mx-auto" max-width="400">
                              <v-toolbar color="green" dark>
                                <v-app-bar-nav-icon></v-app-bar-nav-icon>
                                <v-toolbar-title>Affectés</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <v-btn icon>
                                  <v-icon>mdi-magnify</v-icon>
                                </v-btn>
                              </v-toolbar>
                              <v-list dark>
                                <v-list-item
                                  v-for="(item, index) in assigned"
                                  :key="index"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>{{
                                      item.name
                                    }}</v-list-item-title>
                                  </v-list-item-content>
                                  <v-list-item-action>
                                    <v-checkbox
                                      @change="onChangeAssigned(index, item)"
                                    >
                                    </v-checkbox>
                                  </v-list-item-action>
                                </v-list-item>
                              </v-list>
                            </v-card>
                          </v-col>
                        </template>
                        <template>
                          <v-col>
                            <v-card class="mx-auto" max-width="400">
                              <v-toolbar color="purple" dark>
                                <v-app-bar-nav-icon></v-app-bar-nav-icon>
                                <v-toolbar-title>Disponibles</v-toolbar-title>
                                <v-spacer></v-spacer>
                                <v-btn icon>
                                  <v-icon>mdi-magnify</v-icon>
                                </v-btn>
                              </v-toolbar>
                              <v-list dark>
                                <v-list-item
                                  v-for="(item, index) in agents"
                                  :key="item.id"
                                >
                                  <v-list-item-content>
                                    <v-list-item-title>{{
                                      item.name
                                    }}</v-list-item-title>
                                  </v-list-item-content>
                                  <v-list-item-action>
                                    <v-checkbox
                                      id="available"
                                      @change="onChangeAvailable(index, item)"
                                    >
                                    </v-checkbox>
                                  </v-list-item-action>
                                </v-list-item>
                              </v-list>
                            </v-card>
                          </v-col>
                        </template>
                      </v-row>
                    </v-container>
                  </template>
                </v-row>
                <v-flex xs12>
                  <v-text-field
                    id="assignObs"
                    name="assignObs"
                    v-model="assignObs"
                    :label="$t('assignments.headers.ASSIGN_OBS')"
                    :data-vv-as="$t('assignments.headers.ASSIGN_OBS')"
                    :rules="[() => !!name || 'This field is required']"
                    :error-messages="errorMessages"
                    v-validate.disable=""
                    autocomplete="off"
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="red lighten3" text @click="close" class="btnCancel">{{
              $t('dataTable.CANCEL')
            }}</v-btn>
            <v-btn color="yellow lighten3" text @click="save" class="btnSave">{{
              $t('dataTable.SAVE')
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-flex>
    <template>
      <v-sheet height="64">
        <v-toolbar flat color="dark">
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
            {{ $t('layoutType.LAYOUT_TYPE_TODAY') }}
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="next">
            <v-icon small>mdi-chevron-right</v-icon>
          </v-btn>
          <!-- <spacer></spacer>
            <v-btn outlined class="mr-4" color="grey darken-2" @click="$emit('')">
              <v-icon small>mdi-select-group</v-icon>
              Générer
            </v-btn> -->
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-title>{{ $t('assignments.TITLE') }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-spacer></v-spacer>
          <v-menu bottom right>
            <template v-slot:activator="{ on }">
              <v-btn outlined color="grey darken-2" v-on="on">
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right>mdi-menu-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>{{
                  $t('layoutType.LAYOUT_TYPE_DAY')
                }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>{{
                  $t('layoutType.LAYOUT_TYPE_WEEK')
                }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>{{
                  $t('layoutType.LAYOUT_TYPE_MONTH')
                }}</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>{{
                  $t('layoutType.LAYOUT_TYPE_4DAYS')
                }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-toolbar>
      </v-sheet>
      <v-sheet height="600">
        <v-calendar
          ref="calendar"
          v-model="value"
          :weekdays="weekday"
          :type="type"
          :events="events"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
          @click:day="(event) => dateClick(event, true)"
          :event-overlap-mode="mode"
          :event-overlap-threshold="30"
          :event-color="getEventColor"
          @change="getEvents"
          :locale="locale"
        >
        </v-calendar>
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card color="grey lighten-4" min-width="350px" flat>
            <v-toolbar :color="selectedEvent.color">
              <v-btn @click="editCalendarItem(selectedEvent)" icon>
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <!-- <template>
                  <v-simple-table dense color="selectedEvent.color">
                    <template v-slot:default>
                      <thead>
                        <tr>
                          <th class="text-left">{{ selectedEvent.details }}  &nbsp; &nbsp; {{ selectedEvent.start }} &nbsp; - &nbsp;{{ selectedEvent.end }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(item, index) in selectedEvent.agents" :key="index">
                          <td>{{ item.name }}</td>
                        </tr>
                      </tbody>
                    </template>
                  </v-simple-table>
                </template> -->
              <v-list nav dense :color="selectedEvent.color">
                <v-list-item two-line>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ selectedEvent.start }} - {{ selectedEvent.end }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      {{ selectedEvent.tasks }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      {{ selectedEvent.equipments }}
                    </v-list-item-subtitle>
                    <v-list-item-subtitle>
                      {{ selectedEvent.obs }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  v-for="(item, index) in selectedEvent.agents"
                  :key="index"
                >
                  <v-list-item-content>
                    <v-list-item-title>{{ item.name }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card-text>
            <v-card-actions>
              <v-btn text color="secondary" @click="selectedOpen = false">
                Cancel
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </template>
    <ErrorMessage />
    <SuccessMessage />
  </div>
  <!-- </v-app> -->
</template>

<script>
import { mapActions } from 'vuex'
import { getFormat, buildPayloadPagination } from '@/utils/utils.js'
// import moment from 'moment'
import * as moment from 'moment'
import 'moment/locale/fr'
// import format from 'date-fns/format'
import formatISO from 'date-fns/formatISO'
// import parse from 'date-fns/parse'
import parseISO from 'date-fns/parseISO'
import endOfMonth from 'date-fns/endOfMonth'
import startOfMonth from 'date-fns/startOfMonth'
// import getMinutes from 'date-fns/getMinutes'
// import getHours from 'date-fns/getHours'
// import getYear from 'date-fns/getYear'
// import getMonth from 'date-fns/getMonth'
// import getDate from 'date-fns/getDate'
import { app } from '../main.js'
export default {
  metaInfo() {
    return {
      title: this.$store.getters.appTitle,
      titleTemplate: `${this.$t('assignments.TITLE')} - %s`
    }
  },
  data() {
    return {
      dark: false,
      startMenu: false,
      dataLoaded: false,
      endMenu: false,
      start: null,
      end: null,
      typeToLabel: {
        month: 'Mois',
        week: 'Sem.',
        day: 'Jour',
        '4day': '4 Jours'
      },
      nowMenu: false,
      minWeeks: 1,
      now: null,
      events: [],
      value: '',
      colors: [
        'blue',
        'indigo',
        'deep-purple',
        'cyan',
        'green',
        'yellow',
        'grey darken-1'
      ],
      type: 'month',
      mode: 'stack',
      searchInput: '',
      dataTableLoading: true,
      agentArrayLoaded: false,
      delayTimer: null,
      assignDialog: false,
      search: '',
      pagination: {
        sortBy: this.assignSite,
        order: 'descending',
        page: 4,
        itemsPerPage: 35
      },
      currentItem: '',
      editedItem: {},
      defaultItem: {},
      fieldsToSearch: ['assignAgent', 'assignSite', 'assignTask'],
      isActive: false,
      footerProps: { 'items-per-page-options': [5, 10, 15, 30, 50, 100] },
      focus: '',
      selectedEvent: {},
      selectedElement: null,
      selectedOpen: false,
      selected: [],
      details: null,
      today: new Date().toISOString().slice(0, 10),
      objectIds: [],
      assigned: [],
      agents: [],
      newobjectId: {},
      model: [1, 3, 6],
      assignDateMenu: false,
      startTimeMenu: false,
      endTimeMenu: false,
      assignDates: [],
      assignStartTime: '',
      assignEndTime: '',
      assignTask: '',
      assignSite: '',
      assignEquipment: '',
      enabled: null,
      assignObs: '',
      tasks: [],
      equipments: [],
      weekday: [0, 1, 2, 3, 4, 5, 6],
      weekdays: [
        { text: 'Sun - Sat', value: [0, 1, 2, 3, 4, 5, 6] },
        { text: 'Mon - Sun', value: [1, 2, 3, 4, 5, 6, 0] },
        { text: 'Mon - Fri', value: [1, 2, 3, 4, 5] },
        { text: 'Mon, Wed, Fri', value: [1, 3, 5] }
      ],
      anotherMonth: '',
      snackbar: false,
      snackBarText:
        'Sorry...Not enough Data and/or Computational resources.....',
      errorMessages: [],
      locale: 'fr',
      startDate: null,
      endDate: null
    }
  },
  created() {
    this.agentArrayLoaded = true
  },
  updated() {
    this.$refs.calendar.checkChange()
  },
  components: {},
  // async beforeMount(){
  //    await this.getAssignments()
  // },
  computed: {
    hasIntervals() {
      return (
        this.type in
        {
          week: 1,
          day: 1,
          '4day': 1,
          'custom-daily': 1
        }
      )
    },
    hasEnd() {
      return (
        this.type in
        {
          'custom-cumul': 1,
          'custom-daily': 1
        }
      )
    },
    enable() {
      return (
        this.enabled('header.data-table-select') &&
        this.enabled('item.data-table-select')
      )
    },
    showSelect() {
      return (
        this.isEnabled('header.data-table-select') ||
        this.isEnabled('item.data-table-select')
      )
    },
    hideHeaders() {
      return !this.showSelect
    },
    isLoading() {
      return this.isEnabled('progress')
    },
    assignDateLog() {
      // console.log(this.assignDate)
      return this.assignDate
    },
    formTitle() {
      return this.editedItem._id
        ? this.$t('dataTable.EDIT_ITEM')
        : this.$t('dataTable.NEW_ITEM')
    },
    allAgents() {
      return this.populateAgents(this.$store.state.adminUsers.users)
    },
    // availableAgents() {
    //   return this.fillUserArray(this.$store.state.adminUsers.users)
    // },
    // allShiftTypes() {
    //   return this.$store.state.adminShiftTypes.shifttypes
    // },
    allTasks() {
      return this.populateTasks(this.$store.state.tasks.allTasks)
    },
    allEquipments() {
      // return this.$store.state.equipment.allEquipments
      return this.populateEquips(this.$store.state.equipment.allEquipments)
    },
    allSites() {
      return this.$store.state.sites.allSites
    },
    headers() {
      return [
        {
          text: this.$i18n.t('dataTable.ACTIONS'),
          value: '_id',
          sortable: false,
          width: 100
        },
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_AGENT'),
          align: 'left',
          sortable: true,
          value: 'assignAgent'
        },
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_SITE'),
          align: 'left',
          sortable: true,
          value: 'assignSite'
        },
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_TASK'),
          align: 'left',
          sortable: true,
          value: 'assignTask'
        },
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_START_DATE_TIME'),
          align: 'left',
          sortable: true,
          value: 'assignStartDatetime'
        },
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_END_DATE_TIME'),
          align: 'left',
          sortable: true,
          value: 'assignEndDatetime'
        },
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_OBS'),
          align: 'left',
          sortable: false,
          value: 'assignObs'
        },
        {
          text: this.$i18n.t('common.CREATED'),
          align: 'left',
          sortable: true,
          value: 'createdAt'
        },
        {
          text: this.$i18n.t('common.UPDATED'),
          align: 'left',
          sortable: true,
          value: 'updatedAt'
        }
      ]
    },
    agentHeaders() {
      return [
        {
          text: this.$i18n.t('assignments.headers.ASSIGN_AGENT'),
          align: 'left',
          sortable: true,
          value: 'assignAgents'
        }
      ]
    },
    items() {
      return this.$store.state.calendarItems.calendarItems
    },
    totalItems() {
      return this.$store.state.calendarItems.totalCalendarItems
    },
    allAssignments() {
      // console.log(this.$store.state.adminAssignments.allAssignments)
      return this.$store.state.adminAssignments.allAssignments
    },
    formattedDate() {
      return this.theDate
        ? moment(this.theDate).format('MM/DD/YYYY')
        : undefined // Custom format
    },
    datePickerFormattedDate() {
      return this.theDate
        ? moment(this.theDate).format('YYYY-MM-DD')
        : undefined // Date picker objects needs date in this particular format
    },
    title() {
      const { start, end } = this
      if (!start || !end) {
        return ''
      }
      const startMonth = this.monthFormatter(start)
      const endMonth = this.monthFormatter(end)
      const suffixMonth = startMonth === endMonth ? '' : endMonth

      const startYear = start.year
      const endYear = end.year
      const suffixYear = startYear === endYear ? '' : endYear

      const startDay = start.day + this.nth(start.day)
      const endDay = end.day + this.nth(end.day)

      switch (this.type) {
        case 'month':
          return `${startMonth} ${startYear}`
        case 'week':
        case '4day':
          return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
        case 'day':
          return `${startMonth} ${startDay} ${startYear}`
      }
      return ''
    },
    monthFormatter() {
      return this.$refs.calendar.getFormatter({
        timeZone: 'UTC',
        month: 'long'
      })
    },
    // convert the list of events into a map of lists keyed by date
    eventsMap() {
      const map = {}
      this.events.forEach((e) => {
        (map[e.date] = map[e.date] || []).push(e)
      })
      return map
    }
    // assigned: {
    //   get() {
    //     return null
    //   },
    //   set(value) {
    //     console.log(value)
    //     this.assigned = this.assigned.filter(o => o !== value)
    //     console.log(this.assigned)
    //   }
    // }
  },
  watch: {
    // enabled(slot) {
    //   if (slot === 'no-data') {
    //     this.items = []
    //   } else if (slot === 'no-results') {
    //     this.search = '...'
    //   } else {
    //     this.search = null
    //     this.items = this.agents
    //   }
    // },
    assignDialog(value) {
      // console.log(this.agents.length)
      // console.log(this.agents)
      // if (this.agents.length === 0) {
      // this.Available()
      // }
      // console.log(this.$store.state.adminUsers.users)
      // debugger
      // this.fillUserArray(this.$store.state.adminUsers.users)
      // this.agentArrayLoaded = !this.agentArrayLoaded
      return value ? true : this.close()
    },
    pagination: {
      async handler() {
        try {
          this.dataTableLoading = true
          await this.getAllAssignments(
            buildPayloadPagination(this.pagination, this.buildSearch())
          )
          this.dataTableLoading = false
          // eslint-disable-next-line no-unused-vars
        } catch (error) {
          this.dataTableLoading = false
        }
      },
      deep: true
    },
    async search() {
      clearTimeout(this.delayTimer)
      this.delayTimer = setTimeout(() => {
        this.doSearch()
      }, 400)
    },
    availableAgents: {
      deep: true,
      handler() {
        // console.log('agents in agents: ', this.agents)
        // console.log('selected in agents: ', this.selected)
      }
    },
    assigned: {
      deep: true,
      handler() {
        // console.log('selected in assigned: ', this.selected)
        // console.log('assigned in assigned: ', this.assigned)
      }
    }
  },
  methods: {
    ...mapActions([
      'getAllSites',
      'getAllTasks',
      'getUsers',
      'getShiftTypes',
      'getAllEquipments',
      'getCalendarItems',
      'getAssignments',
      'editAssignment',
      'saveAssignment',
      'deleteAssignment'
    ]),
    // task: item => item.name,
    setLocaleTo(lang) {
      this.locale = lang
    },
    viewDay({ date }) {
      this.start = date
      this.type = 'day'
    },
    getEventColor(event) {
      return event.color
    },
    formatToLocale(d) {
      if (this.locale !== 'en') {
        return `${d.getDate()}/${
          d.getMonth() + 1
        }/${d.getFullYear()} ${d.getHours()}:${d.getMinutes()}`
      }
      console.log(d)
      return d
    },
    showIntervalLabel(interval) {
      return interval.minute === 0
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        setTimeout(() => {
          this.selectedOpen = true
        }, 10)
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }

      nativeEvent.stopPropagation()
    },
    async getEvents({ start, end }) {
      try {
        // const today = new Date().toISOString().slice(0, 10)
        const dateStart = formatISO(
          startOfMonth(
            parseISO(new Date(start.date).toISOString().slice(0, 10))
          ),
          { representation: 'date' }
        )
        const dateEnd = formatISO(
          endOfMonth(parseISO(new Date(end.date).toISOString().slice(0, 10))),
          { representation: 'date' }
        )
        this.events = []
        const snapshot = await this.getCalendarItems({ dateStart, dateEnd })
        for (let i = 0; i < snapshot.length; i++) {
          this.events.push({
            name: snapshot[i].assignSite,
            start: this.formatDate(new Date(snapshot[i].assignStartDate), true),
            end: this.formatDate(new Date(snapshot[i].assignEndDate), true),
            agents: [...snapshot[i].assignAgents],
            color: this.colors[this.rnd(0, this.colors.length - 1)],
            tasks: snapshot[i].task[0].taskName,
            equipments: snapshot[i].equipment[0].equipmentName,
            obs: snapshot[i].assignObs,
            open: false
          })
          // console.log(this.events)
        }
        this.start = start
        this.end = end
      } catch (error) {
        console.log(error)
      }
    },
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    formatDate(a, withTime) {
      return withTime
        ? `${a.getFullYear()}-${
            a.getMonth() + 1
          }-${a.getDate()} ${a.getHours()}:${a.getMinutes()}`
        : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
    },
    saveAssignDate() {
      // console.log('assignDates')
    },
    isEnabled(slot) {
      return this.enabled === slot
    },
    populateTasks(taskArray) {
      this.tasks = taskArray.reduce(
        (accumulator, currentValue, index, array) => {
          accumulator.push({
            text: `${currentValue.taskName}`,
            value: `${currentValue._id}`
          })
          return accumulator
        },
        []
      )
      // console.log(this.tasks)
      return this.tasks
    },
    populateEquips(equipArray) {
      this.equipments = equipArray.reduce(
        (accumulator, currentValue, index, array) => {
          accumulator.push({
            text: `${currentValue.equipmentName}`,
            value: `${currentValue._id}`
          })
          return accumulator
        },
        []
      )
      // console.log(this.equipments)
      return this.equipments
    },
    populateAgents(userArray) {
      if (this.agentArrayLoaded) {
        this.agents = userArray.reduce(
          (accumulator, currentValue, index, array) => {
            accumulator.push({
              id: `${currentValue._id}`,
              name: `${currentValue.firstname} ${currentValue.lastname}`
            })
            return accumulator
          },
          []
        )
        this.agentArrayLoaded = false
      }
      if (this.agents.length === 0) {
        this.agents = [...this.selected]
      }
      return this.agents
    },
    getFormat(date) {
      window.__localeId__ = this.$store.getters.locale
      return getFormat(date, 'iii, MMMM d yyyy, h:mm a')
    },
    async doSearch() {
      try {
        this.dataTableLoading = true
        await this.getAssignments(
          buildPayloadPagination(this.pagination, this.buildSearch())
        )
        this.dataTableLoading = false
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        this.dataTableLoading = false
      }
    },
    buildSearch() {
      return this.search
        ? { query: this.search, fields: this.fieldsToSearch.join(',') }
        : {}
    },
    editItem(item) {
      this.editedItem = Object.assign({}, item)
      this.assignDialog = true
    },
    editCalendarItem(calItem) {
      // console.log(calItem)
      this.assigned = [...calItem.agents]
      this.assignSite = calItem.name
      this.assignTask = calItem.tasks
      this.assignDates = moment(calItem.start).format('YYYY-MM-DD')
      // assignStartDate: calItem.assignStartDate,
      this.assignStartTime = moment(calItem.start).format('HH:mm')
      this.assignEndTime = moment(calItem.end).format('HH:mm')
      // assignEndTime: calItem.assignEndTime,
      this.assignAgents = [...calItem.agents]
      this.assignObs = calItem.obs
      this.assignEquipment = calItem.equipments
      this.assignDialog = true
    },
    async deleteItem(item) {
      try {
        const response = await this.$confirm(
          this.$t('common.DO_YOU_REALLY_WANT_TO_DELETE_THIS_ITEM'),
          {
            title: this.$t('common.WARNING'),
            buttonTrueText: this.$t('common.DELETE'),
            buttonFalseText: this.$t('common.CANCEL'),
            buttonTrueColor: 'red lighten3',
            buttonFalseColor: 'yellow lighten3'
          }
        )
        if (response) {
          this.dataTableLoading = true
          await this.deleteAssignment(item._id)
          await this.getAllAssignments(
            buildPayloadPagination(this.pagination, this.buildSearch())
          )
          this.dataTableLoading = false
        }
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        this.dataTableLoading = false
      }
    },
    close() {
      this.assignDialog = false
      this.agentArrayLoaded = true
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
      }, 300)
    },
    async save() {
      // debugger
      try {
        // const valid = await this.$validator.validateAll()
        // if (valid) {
        this.dataTableLoading = true
        // Updating item
        if (this.editedItem._id) {
          await this.editAssignment(this.editedItem)
          await this.getAllAssignments(
            buildPayloadPagination(this.pagination, this.buildSearch())
          )
          this.dataTableLoading = false
        } else {
          // Creating new item
          await this.saveAssignment({
            assignSite: this.assignSite,
            assignTask: this.assignTask,
            assignDates: [...this.assignDates],
            assignStartDate: this.assignStartDate,
            assignStartTime: this.assignStartTime,
            assignEndDate: this.assignEndDate,
            assignEndTime: this.assignEndTime,
            assignAgents: [...this.assigned],
            assignObs: this.assignObs,
            assignEquipment: this.assignEquipment
          })
          // await this.getAllAssignments(
          //   buildPayloadPagination(this.pagination, this.buildSearch())
          // )
          this.dataTableLoading = false
        }
        this.close()
        // }
        // eslint-disable-next-line no-unused-vars
      } catch (error) {
        this.dataTableLoading = false
        this.close()
      }
    },
    inputHandler(date) {
      if (typeof date === 'string') {
        date = moment(date).toDate()
      }
    },
    // viewDay({ date }) {
    //   this.focus = date
    //   this.type = 'day'
    // },
    // getEventColor(event) {
    //   return event.color
    // },
    setToday() {
      this.focus = this.today
      this.today = this.anotherMonth
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    nth(d) {
      return d > 3 && d < 21
        ? 'th'
        : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
    },
    getIndex(list, id) {
      return list.findIndex((e) => e._id === id)
    },
    getValue(item) {
      return item.toLocaleUpperCase()
    },
    onChangeAvailable(id, item) {
      const index = this.agents.indexOf(this.agents[id])
      // console.log(index)
      const agent = {
        id: this.agents[index].id,
        name: this.agents[index].name
      }
      this.assigned.push(agent)
      // this.$delete(this.$store.state.adminUsers.users, this.agents[index].id)
      this.$delete(this.agents, index)
      this.$emit('onChangeAvailable', this.agents)
    },
    onChangeAssigned(id, item) {
      const index = this.assigned.indexOf(this.assigned[id])
      const agent = {
        id: this.assigned[index].id,
        name: this.assigned[index].name
      }
      this.agents.push(agent)
      this.selected.push(agent)
      this.$delete(this.assigned, index)
      this.$emit('onChangeAssigned', this.assigned)
    },
    async getAvailableAgents() {
      const userArray = this.$store.state.adminUsers.users
      // if (this.agentArrayLoaded) {
      this.agents = userArray.reduce(
        (accumulator, currentValue, index, array) => {
          accumulator.push({
            id: `${currentValue._id}`,
            name: `${currentValue.firstname} ${currentValue.lastname}`
          })
          return accumulator
        },
        []
      )
      return this.agents
    }
    // async generateAssign() {
    //   this.alert('Not enough data.....!')
    // },
    // open(event) {
    //   // window.alert(event.title)
    // },
    // dateClick(event, isAdd) {
    //   // window.alert('date clicked - isAdd?' + isAdd)
    //   // this.today = event.date;
    //   // this.selectedType = 'day';
    //   console.log(event)
    // }
  },
  async mounted() {
    // setTimeout(() => {
    //   this.currentItem = ''
    // }, 2000)
    // const today = new Date().toISOString().slice(0, 10)
    // const dateStart = formatISO(startOfMonth(parseISO(today)), {
    //   representation: 'date'
    // })
    // const dateEnd = formatISO(endOfMonth(parseISO(today)), {
    //   representation: 'date'
    // })
    // const params = { dateStart, dateEnd }
    this.agentArrayLoaded = true
    await this.getAllSites()
    await this.getAllTasks()
    await this.getUsers()
    await this.getAllEquipments()
    await this.getAvailableAgents()
    // await this.getShiftTypes()
    this.$refs.calendar.checkChange()
  }
}
</script>

<style>
table.v-table {
  max-width: none;
}
.controls {
  position: relative;
}
</style>
